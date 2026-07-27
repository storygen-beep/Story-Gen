# Scoring Rubric

How to judge candidates and turn them into a **ranked option set**. Read this during JUDGE.

This file was rewritten because the old version was the named root cause of "the videos are
bad." Its NSFW rubric was Setting 30 / Action 40 / Appearance 20 / Quality 10 — four axes,
none of which asked whether the clip was **alive**. It also scored a wrong room as a
`hard_reject` worth 0. The user's actual winning clip was POV, wrong room, black-and-white
and 264px wide; the old rubric would have binned it at zero before he ever saw it. The
spec-perfect alternative it would have installed instead was correct and dead.

## The one law

**Correctness is binary. Quality is scored.**

Everything about *what is depicted* — act, position, people count, affect, cast, finish, and
POV when the beat needs the partner's body visible — is a **gate**.
You pass or you're out. Nothing about correctness may earn points, because points are how a
correct-but-dead clip out-totals a flawed-but-alive one. Once a candidate is through the
gates it is already correct, so the only thing left to rank on is whether it works.

Two structural consequences, both deliberate:

- `wrong_setting` is **deleted from the hard-reject vocabulary.** A wrong room is now at
  worst a lost 25 points, and when the room isn't load-bearing it isn't scored at all. It can
  never zero a candidate again.
- **Setting may never break a tie.** The old file tiebroke on setting ("settings are rarer
  than actions"). That is exactly backwards and it is gone. Heat breaks ties.

## What you produce — a shelf, not a winner

The deliverable per slot is **one installed best guess + at least 6 stocked options**. You
are a scout stocking a shelf. The human eye is the decider.

| Old behavior | New behavior |
|---|---|
| Pick the highest total above threshold | Rank the whole surviving pool |
| Discard everything below threshold | Stock everything that passed the gates |
| One candidate reaches the human | ≥6 reach the human, in your rank order |
| Accept thresholds 60 / 70 | **No accept threshold exists.** Deleted. |

The thresholds are gone because their only job was to trigger the critique loop, and a
threshold cannot do that job without throwing away the pool. The new trigger is **shelf
depth**: fewer than 6 survivors → go back and search more. Never lower a gate to fill the
shelf; that ships a wrong clip. Broaden the query or change source instead.

You may never: auto-pick silently, present a single candidate, install an **animated** pick you
have not frame-stripped, or drop a candidate for any reason other than a named gate failure.

## Format — animated vs static is ACTION-driven, not tier-driven

Confirm before scoring. Kiss / tease / undress / flash / bathing / any explicit act → animated
(`.webm` / `.gif` / `.mp4`); a still loses the chemistry. Domestic / conversational / location
/ object / light-flirt → `.jpg`; a looped GIF of a dinner is noise. Full matrix in SKILL.md
§Format classification. The download API sets the saved extension from the SOURCE URL and
ignores what the TOML declared, so this rule really means *pick the right kind of source*.

---

## Gate 1 — CAST (judge from the thumbnail, it's cheap)

These come from the TOML's character definitions via the scope brief. They are kept from the
previous rubric nearly verbatim because they were right: they describe *who may be on screen*,
which the narrative fixes in advance.

- **Solo** (no partner interaction) when the beat is a two-person scene
- **Same-sex couple** when the game requires M/F — check NPC gender in the TOML
- **BDSM gear** (ropes, paddles, gags, restraints, crops, blindfolds, harnesses) absent from
  the narrative — domestic scenes don't involve kink unless the beat says so
- **Interracial mismatch** vs the NPC description in the TOML character section
- **Visibly 40+** (mature/MILF-tagged) when the character is in her 20s–30s
- **BBW/SSBBW** when the NPC is described petite or average
- **Cosplay / costumes / uniforms** in a casual or domestic scene — a schoolgirl outfit in a
  "morning coffee" beat is wrong
- **Extreme / fetish content** (rough, gagging, choking, facial) when the beat is tender
- **Children or families** — never, on any tier
- **Face filters** (Snapchat-style beautifiers, dog ears, skin smoothing) — they read as
  phone-app footage and break the fiction instantly
- **Obvious AI-generation artifacts** — wonky hands, smeared faces, impossible geometry
- **Heavy watermark across the subject** — corner watermarks are fine, these are placeholders

**People count is now bound to the beat, not to a constant.** The old filter was a blanket
"3+ people = reject." That filter shipped a documented defect: a beat calling for a *crew*
needs a visible 3+, and 1–2 men failed it. So the rule is now **count ≠ the beat's declared
count → reject**, in either direction. Two people when the beat says three fails. Three when
the beat says two fails. The brief declares the number; you match it.

SFW equivalents, unchanged: crowds where the beat is private, a restaurant when the query
said *home* kitchen, and — for `location_image` — people dominating a frame whose subject is
the space; for `clothing_image`, an editorial model wearing the item instead of the item.

## Gate 2 — the FRAME STRIP (mandatory for animated finalists, route-independent)

**Scope, stated once so nobody has to guess.** A frame strip is a claim about a *loop*, so it
exists only for animated finalists — `.webm`, `.mp4`, `.gif`. A `location_image` or
`clothing_image` `.jpg` has no loop to strip; those finalists are judged from the contact
sheet, and that is complete verification for them. So: **every animated finalist is
strip-verified; static finalists are judged from the contact sheet.** Anywhere you read an
unqualified "never install anything you have not frame-stripped", read it as that.

**Thumbnails lie, constantly.** Measured this session across two rounds: the strip killed
**3 of 5** and **4 of 6** shortlisted candidates. Roughly one in three survives. Documented kills:

- a thumbnail showing a perfect cluttered back room whose loop was standing **kissing**, no
  blowjob anywhere in it
- a "dark outdoor" thumbnail whose loop was a bright daytime **laundromat**
- a thumbnail that read bent-over-from-behind but whose loop was a **blowjob**

So: **for animated candidates you score the strip, never the thumbnail.** Build it with
`video_frames.py --mode strip --frames 4` (see `references/clip_preranking.md`). This applies
to every retrieval route without exception — the strip is about what the file contains, and
files lie the same way whatever site they came from.

Budget rule, because stripping is the expensive step:

1. **Animated mode: strip the top 6 by contact-sheet rank.** Six is the canonical number —
   it is the same six as the minimum shelf depth, and it reliably covers the installed pick
   and its nearest alternates. If another file names a different count, this one is right.
2. **Static mode: strip nothing.** Zero is the canonical number there. Judge `.jpg`
   finalists from the contact sheet and install from that.
3. If fewer than 2 of those 6 survive Gate 3, your query is wrong, not your luck — re-query
   before stripping more.
4. Everything you do not strip is still **stocked** (it was stocked back in STOCK, before any
   judging), tagged `verified: "thumbnail"`, so the human knows which alternates are unproven.
   An unverified-but-promising clip belongs on the shelf; binning it is the disease this
   rewrite exists to cure.
5. **Never install an animated pick unstripped.** The installed pick goes into the game unseen
   by a human; it is the one file that must be proven.

## Gate 3 — the BEAT (judge from the strip; from the contact sheet for static items)

Every one of these is a documented rejection from this game's history. They are checks, not
scores.

| Check | Fails when | Why it's a gate |
|---|---|---|
| **Act** | The beat says his hand; the clip shows a cock | A different act is a different scene |
| **Position** | Beat says kneeling, clip is standing; beat says from-behind-passive, clip is supine-performing | Position carries who is doing what to whom |
| **Count** | See Gate 1 — beat's count, either direction | A crew that isn't a crew reads as a different story |
| **Affect** | Bright smiling performer when the beat is forced / used | Affect is the beat's meaning; a happy performer rewrites it |
| **Extra people** | Anyone present the beat doesn't have | Same failure as count |
| **Finish** | Beat calls for a finish, the loop never shows it | The clip promises and doesn't pay |

**Affect is a gate here and an axis in HEAT — that is not a contradiction.** The gate asks
*is it the right affect*; the axis asks *how strongly is it there*. Wrong affect is out;
right-but-limp affect is scored low, not rejected.

### POV — two cases, never a blanket reject

POV is a **defect** when the scene's meaning needs the partner's body seen. Test: *does the
meaning live in the partner's body?* A slack, limp, passed-out, watching, restrained or
pointedly-still man **cannot be the camera** — if he's the camera, the thing the beat depicts
is off-screen. Counting men is the same problem: you can't count a crew you can't see. Those
fail Gate 3.

POV is **fine, often stronger**, when the clip's power is her face and her eyes aimed at the
viewer. POV puts the camera where the player is, so eye contact into the lens is eye contact
with the player — the strongest available form of the one heat signal we have confirmed.

When POV is not a Gate-3 failure it must not be penalized on any axis. The winning clip was POV.

---

## The axes

Exactly three axes — **HEAT, SETTING, CRAFT** — always summing to 100. The **setting axis is
conditional**: when the room isn't load-bearing you don't score it low, you **don't score it at
all**. Its whole weight moves into heat, which says the right thing out loud — when the room is
disposable, aliveness is nearly everything.

| Axis | `setting_is_load_bearing = true` | `= false` |
|---|---|---|
| **HEAT** | 60 | **85** |
| **SETTING** | 25 | **skipped — record `setting: null`** |
| **CRAFT** | 15 | 15 |

There is no fourth axis. Correctness — act, position, count, affect, cast, finish, and
POV-when-the-partner-must-be-visible — is a gate, and gates never contribute points.

### HEAT (dominant)

Whether the clip is alive. Four observable signals — observable specifically **from a frame
strip**, which is why they're written this way:

1. **Eye contact held across the loop.** She looks at the camera, and she's still looking at
   it in frames 2, 3 and 4. This is the one signal confirmed by a direct head-to-head. Two
   candidates died this session on wandering eyes their thumbnails hid — which is exactly why
   "held across the strip" is in the rule and "present in a frame" is not.
2. **Affect at intensity, matching the beat.** Not "more enthusiasm is better" — the *asked-for*
   affect, strongly. An eager beat wants visible want; a used beat wants visible blankness. A
   performer running through it is dead on either.
3. **Energy.** Something is happening across the four frames. A held pose tiled four times is
   a photograph with extra steps.
4. **Framing intimacy.** Close enough to read a face and a body. A wide, distant,
   everything-in-shot composition is colder than a tight one at the same act.

**Honesty about these four.** Only signal 1 is proven — one clean head-to-head plus two
rejections. Signals 2, 3 and 4 are *derived from a documented rejection history*, never A/B
tested, and a fresh study will refill them. Weight your judgment accordingly: when the eyes
are the only thing you're sure of, trust the eyes, and when heat is ambiguous, stock rather
than decide. See the Confidence table below.

| Band | Signals present | Load-bearing (of 60) | Setting skipped (of 85) |
|---|---|---|---|
| **ALIVE** | 3–4 | 48–60 | 68–85 |
| **WORKING** | 2 | 30–45 | 42–64 |
| **DEAD** | 0–1 | 0–18 | 0–25 |

**Worked examples.**

- **ALIVE, and it won.** POV, wrong room, black-and-white, 264px. It won on eyes: she holds
  the camera the entire loop. Signals 1, 2 and 4. The user's own words were that "the eyes
  made it win." Resolution did not participate in this decision, and neither did the room.
- **DEAD, and it lost.** Spec-perfect: right act, right position, right room, clean and sharp.
  Nobody in it was present. Zero of four signals. Under the old rubric it scored near the top
  and was installed.
- **WORKING.** Right affect, real motion, but her eyes are down or away for most of the loop
  and the framing is wide. Signals 2 and 3. This is a legitimate stocked option and a
  legitimate install when nothing better exists — it just loses to an ALIVE clip with worse specs.

### SETTING (conditional)

The scope brief carries `setting_is_load_bearing`. The test: **does the room carry danger,
secrecy, or squalor** — would the beat *mean something different* in a clean bedroom?

- **Load-bearing (25).** A dark alley: bright clips were rejected twice there, because the
  darkness is what carries the danger. Score it hard — 20–25 for the described environment,
  0–5 for a room that fights the beat.
- **Not load-bearing — skip the axis.** Do not score it low, do not score it at all: write
  `setting: null` in `scores.jsonl` and give heat the full 85. The user, on a beat where the
  assistant had been hunting rooms: the setting "doesn't matter much here." A skipped axis
  costs a wrong room exactly nothing, which is the point — and it leaves no small residue for
  a spec-perfect dead clip to win on.

When you write queries, this flag also tells you where to spend words: spend on setting only
when it's load-bearing, otherwise act + position + heat lead. See `references/query_rewriting.md`.

### CRAFT (15)

Only one question: **can you read what's happening?** Nothing else.

- Legible: the act is unambiguous in the strip (in the image, for static items) → 10–15
- Murky: motion blur, extreme darkness, or a crop that hides the act → 0–8
- **Resolution is not a gate and barely an axis.** A 264px clip won. Reads-at-264px beats
  unreadable-at-1080p every time.
- Watermarks in a corner cost nothing — these are placeholders.

Resolution *does* cost real craft points on `location_image` and `clothing_image`, and only
there: a navigation image renders large and static, so softness shows. A clip renders small
and loops. Judge them at the size they ship.

### SFW items

Same shape, different vocabulary. Subject correctness moves into the gates (a kitchen image
must be a kitchen; a location shot must not be dominated by people; a clothing shot must show
the item, not a model). What's left to score:

| Axis | Weight | What you're looking at |
|---|---|---|
| **LIFE** (heat's SFW name) | 50 → **75** when setting is skipped | Does it look lived-in and specific, or like a stock render of the concept |
| **SETTING** | 25 → **skipped, `null`** | Same conditional test as above — skipped, never scored low |
| **CRAFT** | 25 | Resolution, framing, no AI artifacts — these render large |

For `clothing_image` and flat-lay product shots there is **no life analog** and you should not
invent one. Those collapse to subject legibility + craft. Honesty beats symmetry.

---

## Do not award half credit

If the beat says kitchen, the kitchen is load-bearing, and the strip shows a generic bed, then
setting scores 0–5, not 12 — and if the kitchen isn't load-bearing there is no score to award
at all, because the axis is skipped. If the beat wants forced and the performer is neutral,
that's not "half the affect" — affect is a Gate-3 check and neutral-when-forced fails it.
Near-misses that get half credit accumulate
into a total that outranks a clip which is actually right. The bands exist to stop that.

Likewise on heat: **one lucky eye-contact frame is DEAD, not WORKING.** The signal is defined
as *held across the loop* precisely so it can't be earned by a good thumbnail.

## Ranking, the dead-clip veto, and installing

1. Rank all gate-survivors by total, descending.
2. **Dead-clip veto.** If the top-ranked option is in the DEAD heat band, do **not** install
   it. Install the highest-ranked ALIVE or WORKING option instead, even though its total is
   lower. This is the structural guarantee: a correct dead clip can never beat a flawed live
   one, no matter how the other axes fall.
3. If the *entire* pool is DEAD, install the best of it, mark `pool_all_dead: true`, and tell
   the human plainly. A dead shelf is a query problem — re-search before you accept it.
4. **Ties break on heat**, then on craft. Never on setting.
5. Install rank 1 via `grab` (POST `{game,file,url,source}`). Say out loud in your report that
   this is a best guess, not a verdict.
6. **Do not stock here. Nothing.** Stocking already happened, once, in STOCK — immediately
   after extraction and before any judging — which is exactly what makes the runner-ups
   survive a harsh judge. JUDGE ranks and installs; JUDGE does not stock. The installed pick
   is already on the shelf from STOCK, so there is nothing left to POST.
7. A refetch **rebuilds** the option set, and the order is **stock first, prune after —
   never clear on the way in**:

   1. `t0 = now()` in ISO — record it before you fetch anything.
   2. Harvest and stock the new candidates as usual.
   3. Only then `POST options/clear` with `{game, file, before: t0}`.

   The backend supports `before`, and entries with `origin: "previous"` always survive the
   clear, so the human keeps his undo history. Do **not** walk `options/list` and
   `options/remove` each stale url — that loop deletes the history along with the staleness.
   And never clear before the replacements exist: wiping first once silently ate three
   harvests, which is why this order is written down.

## `scores.jsonl`

One JSON object per line, at `games/<game>/.find-media/evidence/<item_id>/scores.jsonl`.
Losing scores are kept — see below for why.

```json
{"candidate_id": "blovjob/alley-behind-the-club", "url": "https://blovjob.com/content/2023/11/panties-down-in-an-alley-behind-the-club.gif", "strip_path": "evidence/alley_bj_t5/strip_alley_behind_the_club.jpg", "verified": "strip", "gate": "pass", "pov_case": "fine_face_forward", "heat_band": "alive", "heat": 74, "setting": null, "craft": 13, "total": 87, "setting_load_bearing": false, "decision": "installed", "note": "holds camera all 4 frames"}
{"candidate_id": "nsfwgify/53980631", "url": "https://cdn.nsfwgify.com/53980631/kneeling-outside-at-night.gif", "strip_path": null, "verified": "thumbnail", "gate": "pass", "heat_band": null, "heat": null, "setting": null, "craft": null, "total": null, "decision": "stocked", "note": "unstripped alternate, rank 8"}
{"candidate_id": "hardcoregify/44120033", "url": "https://cdn.hardcoregify.com/44120033/against-the-wall.gif", "strip_path": "evidence/alley_bj_t5/strip_against_the_wall.jpg", "verified": "strip", "gate": "fail", "gate_reason": "act:kissing_not_oral", "decision": "gate_reject"}
```

`decision` ∈ `installed` | `stocked` | `gate_reject`. `verified` ∈ `strip` | `thumbnail`.
`gate_reason` is `cast:*`, `act:*`, `position:*`, `count:*`, `affect:*`, `finish:*`, `pov:*`.

Note the installed row: `setting_load_bearing: false`, so `setting` is `null` — skipped, not a
low number — and `total` is heat + craft out of 100. A row that carries a small setting score
on a non-load-bearing beat is a row scored under the old rules.

Note also the hosts: no `*.phncdn.com` url ever appears here, because a PornHub-hosted result
is read for its title and tags and then **skipped as a candidate** — it is never queued for
download. See `references/media_sources.md`.

**`wrong_setting` is not a valid `gate_reason`.** If you find yourself writing it, you have
reintroduced the bug this file was rewritten to kill.

## Confidence — which of this is proven

Be honest about the evidence, because a future reader needs to know what to trust and what to
overwrite.

| Rule | Evidence | Status |
|---|---|---|
| Eye contact held across the loop carries heat | One direct A/B: the user's pick beat a spec-perfect alternative explicitly on the eyes; two further candidates rejected for wandering eyes their thumbnails hid | **Confirmed**, n=3 events, one of them a clean head-to-head |
| Thumbnails lie ~2 of 3 times | 3/5 and 4/6 killed on the strip, two independent rounds | **Confirmed**, n=11 |
| Setting is conditional | Two beats, opposite calls, both explicit from the user (alley = load-bearing, other = "doesn't matter much here") | **Confirmed**, n=2 |
| Gate-3 checks (act / position / count / affect / extra people / finish) | Every one is a logged rejection from this game's history | **Confirmed** as rejection classes |
| Heat signals 2, 3, 4 (affect intensity, energy, framing) | Inferred from the rejection history, never A/B tested | **Provisional** |
| Band boundaries and the 60 / 25 / 15 split (85 / 15 when setting is skipped) | Chosen to make the documented win beat the documented loss | **Provisional** |

A fresh 10-query study will refill this table. Until it lands, follow the two survival rules:
**when heat is ambiguous, stock more options rather than deciding** — the shelf exists exactly
for the cases the rubric can't call — and **do not tune the weights to make a past pick come
out right.** These numbers order a shelf. They don't prove anything.

## Why scores live on disk

Persistence isn't bookkeeping overhead. It unlocks:

- **Resume** — an interrupted batch restarts by reading `scores.jsonl` and skipping already-scored candidates
- **Telemetry** — `run_manifest.json` aggregates score distributions across items, revealing whether queries were systematically weak or sources were thin
- **Audit** — a human reviewing a questionable install can read the rejected candidates and their gate reasons
- **Cross-source learning** — after 10 games, aggregated scores per source tell you which sites actually deliver for your typical beats
- **Heat calibration** — this is the new one, and the most valuable. `scores.jsonl` is the
  *prediction*; the review store (`media_reviews.json`, approved / disapproved) is the human's
  *ground truth*. When he disapproves your install and grabs stocked option #4 instead, that
  pair is a labeled heat error. It is the only dataset that will ever validate or kill the
  provisional rows in the Confidence table.
