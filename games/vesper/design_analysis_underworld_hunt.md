# Vesper — Design Analysis & Locked Design: The Underworld Hunt (Act 2 On-Ramp)

> **What this doc is.** The design record for Vesper's next chunk, capturing (a) the mopoga review +
> our analysis, (b) the gap we found, (c) the locked design of the underworld hunt, and (d) the
> engine/save-safety findings that constrain how it's built. Everything below is grounded in evidence
> gathered on 2026-07-08 (two verified sub-agent workflows + direct code/TOML reads); key citations
> are inline. The design half (§4) folds into `design_book.md` when authoring begins.

---

## Context — why this change is being made

Vesper shipped and drew a mopoga reviewer verdict:

> *"The game has a solid overall structure, but it lacks content. In my tests, the gameplay boiled
> down to resource grinding rather than focusing on the adult content. I recommend resubmitting the
> game after a few more updates."*

We ran an honest diagnosis (is this true? where? is it the game, the skill, or the engine?), then
worked out the highest-leverage fix and locked the next chunk to build. The intended outcome: a
resubmittable Vesper whose next stretch of play is **content, not grind**, plus a clear record of
*why* so we don't re-ship the same problem.

---

## 1. The review, and our diagnosis

**The reviewer is half-wrong on volume, exactly right on the feel — and we can point at where.**

By canvas payload Vesper is **16 adult / 12 grind / 24 nav-utility** (52 total). It *opens* with a
fully explicit sex scene at zero grind (`2_one_shots.toml:14-128`), and Mercer is a repeatable
explicit sex loop reachable immediately after the opening with **no** resource gate
(`5_scenes.toml:16-77`). So "lacks content" as a raw-volume claim is **refuted** — there is more
built erotic content than grind content, and a meaningful slice is ungated.

**But the felt experience is real and correctly located.** The one arc that *is* the designed
gameplay — the Renner infiltration — walls its first *earned* payoff behind roughly **22
charge-throttled actions**:

- ~7× `work_depot_haul` (+3 relation each) to reach relation 21, which opens his office
  (`5_scenes.toml:630`)
- then ~15 seduction rungs (+2 corruption each) to reach corruption 30 for the first blowjob
  (`5_scenes.toml:772`); corruption 40 gates the loop, 50 gates the anal "drain"
- every rung/shift costs 15 Charge inside a 09:00–18:00 window → ~3 rungs/day across **5–7 in-game
  days**

Between those sparse payoffs, the entire interactive surface **is** resource loops (haul for
relation, rungs for corruption, drill for fighting, cradle for charge). So the part a first-time
player actually *plays* between the porn does boil down to grinding toward gated beats.

**Verdict: CONFIRMED for the mission arc, REFUTED as a whole-game claim.** It's a **placement +
ratio + roster** problem, not a word-count shortage.

*(Nuance we corrected mid-analysis: the tease/flash/grope rungs are NOT empty meter-ticks — each is
a real little scene with video + reaction dialogue that escalates by corruption band,
`5_scenes.toml:408-455` + the rung canvases. The genuinely content-free grind is (a) the ~7 crate
hauls before the office even opens, and (b) re-seeing the same 3 rung scenes ~15× to climb the
number.)*

---

## 2. The gap (the core finding)

**The game runs out of people before the story is over.**

- **Two NPCs.** Mercer (owner — flat by design, no arc) and Renner (Mission-1 target). Once Renner
  is drained, he's *done*; Mercer never develops. Genre floor for an adult sandbox is **10–20**
  developed NPCs (RTS, the mopoga flagship, runs ~10 deep arcs + 71 location scenes).
- **The story promises more and then hits an empty room.** Renner's drain literally points the
  player into the underworld to hunt the next people (`5_scenes.toml` renner_control_canvas) — but
  the second act (**Bastien, Calloway, Cain**) is designed in `design_book.md` (lines 147-158,
  254-262, 320-326) and **never built** (zero canvases).
- **The underworld is a faceless shell.** It's reachable off the Waterfront with a coin economy,
  pit fights, market, and a brothel *sex loop* — but no named target and no arc; the brothel is
  cold transactional filler.

**This is also a skill-level defect, not just a Vesper slip.** Vesper *followed* the author-game
skill correctly (still-point protagonist declared → the feeder-content economy dissolves "by
design", Step 6 graded GO). The skill's still-point exemption removes the content-density floor and
installs no replacement, and `step-3-casting.md` permits a 2-NPC cast. So a correct skill would NOT
have prevented this → **the skill must also be fixed or the next still-point game re-ships the same
review.** (Tracked as a separate work item; see §7.)

---

## 3. The strategic answer (breadth vs depth)

LO's question was: add more parallel things to do (breadth) or write more of the same, deeper
(horizontal depth)? **Neither, as framed:**

- **Depth-of-same is wrong** — volume isn't the problem; more scenes on the same 2 arcs leaves the
  grind spine untouched.
- **Breadth-of-activities is the trap** — more loops/activities = more grind = the exact complaint,
  worse.

**The fix is breadth of _people_ + re-placement:** build the missing second act, and wire the grind
to *deliver* content rather than gate it (RTS fires ~47% of a core NPC's scenes from inside ordinary
routine activities — the routine IS the pipe). For this chunk specifically: **build the hunt that
reveals Bastien**, then (later) Bastien's arc.

---

## 4. Locked design — The Underworld Hunt (Act 2 on-ramp)

### 4.1 Frame
This chunk is **the hunt** — the player *collecting pieces* to **discover** Bastien. She does not
know his name at the start; the payoff of the chunk is that the trail finally drops his name and
location. **Bastien's own arc (seduce/flip/drain) is the NEXT chunk, not this one.**

Design principle (so it doesn't become a fetch-quest): **every stop is a scene / small conquest, not
a clue-counter**, and the chain **lands on Bastien** — it never drifts into a dead side-room. The
one test: *is the player getting a scene here, or just a signpost?* Signposts get cut or merged.

### 4.2 The beat chain — LOCKED (steps 1–6)
1. **Renner's drain** hands her **two names** (the two men he killed) + "they came out of the
   underworld." *(Names are NEW — added to the drain; see §5.)*
2. She works the underworld → an **informant** knows one name ran for the company early on, and
   points her at a **third guy** — the one thing he knows: that guy hits **The House every Sunday**.
   *(Uses the schedule system — targets on timetables make the world bite.)*
3. **Sunday at the brothel:** the third guy is there for **one specific girl**. She schemes the girl
   off the board (**Axis A** — a real beat; introduces a new girl), takes her slot, **serves him —
   and drains him.** *(Bastien's unseen eyes clock her here — a planted watcher, so the later grab
   is earned, not a gotcha.)*
4. The drain gives up **where the crew lived.** She goes there.
5. There she finds the name — **Bastien** — and in the same beat **his people take her.**
6. **Face to face:** he knows she's hunting him, and he knows she's **Mercer's — because his
   connections told him** (he is a man of connections; **not** via Cain). He wants to know why she's
   really here. **← lock ends here. Captivity / the flip / the Cain reveal = a later chunk.**

### 4.3 Bastien (established here; his arc built later)
- **Who:** the docks dealer who supplies Cain — owner of the **bar and the brothel both**, works
  from behind, handles things through a web of connections.
- **Secret (saved reveal):** he **works with Cain**, for Cain's cause, within his own limits. Kept
  OFF the kidnap beat so it lands later as its own bombshell (second crack in "Cain is evil"; the
  first crack was Renner's drain).
- **Shape:** NOT a seduce-in target like Renner/Calloway — a **capture-and-flip.** Her cover is
  useless against him from the jump. This is deliberate *variety* — three identical infiltrations
  would be the repetition we're trying to kill.
- **Casting revision:** his `design_book.md` entry changes from "the newcomer's submissive cover"
  to "the underworld owner who catches her, aligned with Cain."

### 4.4 Why this serves the fix
New *person* (the roster fix), delivered as **hot beats** (scheme → serve+drain → walk into the
trap), the **world initiates** (Bastien hunts her back — prey, not just predator), it **advances the
mystery**, and it **varies the conquest** (capture-flip ≠ seduce-in).

---

## 5. Engine & save-safety findings (verified in code this session)

### 5.1 The problem
Renner's drain currently says *"two of my people"* — **no names** (`renner_control_canvas`, the
"Why did Cain burn you down?" beat). The burned-yard find (`yard_find_3`, `3_activities.toml:698-720`)
gives **two faceless files + underworld origin** — also no names. So the hunt has nothing concrete to
start from. **Fix:** Renner names the two men at the drain.

### 5.2 How the names enter game state
Names are spoken at the drain, and the drain flips **one new hidden marker — a TRAIT** (e.g.
`names_known`, default 0). The underworld hunt is gated on that marker. Drain → hear names → marker
flips → hunt opens.

### 5.3 The load-bearing rules (each verified)
- **Names + marker must go on BOTH drain branches**, not just the first. The drain has a first-time
  full branch (`.intro`, `drains_done lt 1`, which today sets `renner_drained` +
  `renner_leads_extracted`, `5_scenes.toml:1056-1068`) and a repeat branch (`.again`/`.again_ask`,
  `drains_done gte 1`, which today **sets nothing**, `1069-1088`). A returning player who already
  drained has `drains_done >= 1` and can **only** reach the repeat branch — so names/marker placed
  only on `.intro` would never reach them.
- **Use a TRAIT, not a flag, for the marker.** The drain setter (`loop_renner_finisher`) is
  *triggerless*, and the flag-chain validator **hard-fails the build** ("MISSING HINT",
  `v2.py:11220-11286` → `package_from_toml.py:385-399`) if a new flag is required `is_true` by a
  canvas trigger/choice whose setter has no location. Traits are never location-checked. This is
  exactly why the game already branches the drain on the `drains_done` **trait**, not the
  `renner_drained` flag (see the TOML comment at `5_scenes.toml:1052`).
- **`version = "1.0"` on every new conditions block**, or it fail-opens (`v2.py:3653` returns true
  for any block missing/≠ `"1.0"`) and the hunt shows from game start — a build-green failure only
  live play catches.
- **No separate "invalidation flag" is needed.** Gating the hunt on one new marker (default 0) gives
  "the old drain means nothing" for free: old saves backfill the marker to 0 → hunt locked until a
  fresh drain; the old drain never set it because it didn't exist.

### 5.4 The save reality (verified — returning players KEEP their progress)
The default build is the **no-DB in-memory graph** (`package_from_toml.py:168`, no-DB unless
`--use-db`), and it assigns **stable slug ids** to NPCs (`game_graph.py:144`, `npc.id = n.id`) plus a
stable slug-derived project id (`:82`, `uuid.uuid5`) — the code comment states this *"fixes `$npcs`
save-survival"* (`:81`). **Ground-truth confirmed in the built game:** Vesper's `index.html` keys
`$npcs` by `npc_mercer` / `npc_renner` (slugs), with zero UUIDs. So NPC ids do **not** regenerate on
rebuild, and a returning player who drained Renner in the old version **keeps** his relationship /
corruption after loading into a rebuilt version. Player flags/traits also survive (the fill-if-absent
backfill seam, `v2.py:14668-14735`).

**Implication:** returning players keep their progress across an update — Renner stays drained and
ready, so re-draining to pick up the new names is trivial. (The old "NPC state resets on rebuild"
behavior was the **legacy `--use-db` path** — real DB rows with random `uuid4` ids — which is *not*
the default and not how Vesper is built.) The names plan is unchanged: names + marker on both drain
branches, gated on a trait (the trait choice is for the flag-chain validator, not the save layer).

---

## 6. Build sequence (propose-first; one verified piece per turn)

All authoring goes through source phases → merge → package; **never hand-edit `7_final_game.toml`.**
Vesper is **shipped**, so **extend only** — no renaming existing ids/keys/stat-scales/title
(`save-safety`).

1. **Design into `design_book.md`** — Bastien's revised casting entry (§4.3) + the hunt beats (§4.2)
   in plain words. LO reviews intent first.
2. **Names + marker** — add `names_known` trait (`0_systems_spec.toml`, init in
   `1_metadata_and_locations.toml`); weave the two names into `.intro` **and** `.again`/`.again_ask`;
   set `names_known = 1` on **both** drain-routing choices.
3. **Author the hunt** — informant → the third guy on a Sunday schedule at The House → the girl
   scheme (Axis A) → serve + drain the third guy → the crew's place → find "Bastien" → the kidnap
   capstone (auto-fire, `is_repeatable=false`, single Continue). Gate hunt content on
   `names_known gte 1` with `version="1.0"` on every block.
4. **Merge + green build + live-test both cohorts** (fresh save; and an old-save sim with
   `drains_done>=1` → re-drain → names on the repeat path → marker flips → hunt opens). Reload after
   rebuild only to pick up new content — NPC state persists (stable slug ids; see §5.4).
5. **Later chunks (not now):** Bastien's captivity/flip arc; Calloway (Mission 3); the site/chip
   ending.

**Separate track (so it doesn't recur):** patch the author-game skill — a lewd-payoff-cadence floor
distinct from thread-count, a still-point replacement content floor, and a who-climbs-tied cast
floor (`content-framework.md §1B/§2F`, `step-3-casting.md`, `step-6-feedback.md`).

---

## 7. Open items / decisions for LO
- **The two dead-men names** — to be picked (underworld-grimy, consistent with the world) unless LO
  names them.
- **Brothel access** — locked to **Axis A** (displace the girl); Axis B (climb the sex-worker tier)
  only as light flavor if wanted, never a full promotion-grind.

---

## Verification (once we build)
- **Green build**: `scripts/merge_toml_phases.py` then `manage.py package_from_toml` — passes because
  the hunt gate is a trait (not a flag on the triggerless finisher) and every new conditions block
  carries `version="1.0"`.
- **Live-test (headless SugarCube harness)** two cohorts:
  1. *Fresh save* — drain Renner once → names appear in `.intro`, `names_known` flips, the underworld
     hunt unlocks; walk the chain informant → Sunday brothel → girl-scheme → serve+drain → crew place
     → find "Bastien" → kidnap fires.
  2. *Old-save sim* — set `drains_done >= 1` with Renner's earned state INTACT (stable slug ids
     survive the rebuild — §5.4); re-drain via the repeat branch → names appear in `.again_ask`,
     `names_known` flips, hunt unlocks.
- **Confirm** the kidnap capstone is a single-exit auto-fire (no dead-end) and that no new gate
  fail-opens (nothing from the hunt is visible at game start).
