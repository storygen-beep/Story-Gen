# author-game skill — improvement backlog

*A living working document. Derived from a full analysis of the **Vesper** build (the 76-entry `decisions_log`,
the curated `iteration-log.md`, the design-book "added during authoring" sections, the 10K-line transcript,
memory, and a structural self-audit of the skill). 47 raw findings → 26 verified themes → the 25 actionable items
below (+ 1 follow-up discovered during execution).*

**Every item is cited both ways** — the Vesper evidence (`decisions_log[#]` / design_book § / iteration-log /
transcript / memory slug) **and** the current skill file:line proving its state. LO's rule #1: no claim without a
citation.

**Status legend:** ✅ done · 🔨 in progress · ⬜ open
**Priority:** P0 (load-bearing, recurs every game) → P3 (nice-to-have) · **Effort:** S / M / L
**Layer:** `skill` (doctrine taught wrong/incompletely/not-at-all) · `engine` (substrate gap the skill should
still document) · `process` (how Claude works) · `one-off` (author slipped; skill was right)

---

## Progress log (newest first)

- **2026-07-04 — ✅ #1 reframed + done (systems grow through iteration).** Instead of a day-one system checklist
  (wrong — sandbox systems emerge from play), shipped a *reach-for-it* recipe menu (`references/system-patterns.md`,
  7 recipes) + a mid-stream fold-in loop with **"playable ≠ done"** (`run-mode.md`), wired into `SKILL.md` /
  `step-2-toplevel.md` / `systems.md`. #2–#7 now have starter recipes in the menu. Uncommitted; CHANGELOG 07-04.
- **2026-07-02 — ✅ #8 clamp-or-vanish lint (DONE).** Hardened the banded-stat clamp doctrine across 5 reference
  files + CHANGELOG. Verified: engine facts read from `v2.py`; grep-consistency across `references/` (no surviving
  "recommended on a restore" / bare-`+N` counter-example); the two load-bearing cites re-checked after the engine
  renumber. *Status:* the 5 reference files are edited + verified but **uncommitted** in the working tree; the
  CHANGELOG entry was committed in `6b07567`. **Commit the 5 reference files when convenient.**
- **Engine work that landed mid-analysis (parallel session):** `8446b3d` (no-DB build pipeline + constant slug
  IDs), `1d9ce93` (save-safe releases — slug passage names + save-migration seam), `6b07567` (save-safety
  authoring doctrine + stale-fact fixes). These **renumbered `v2.py`** (→ see #26) and **largely answered the
  save-compat question** (→ see "Related open thread").

---

## The meta-pattern (read first)

Three failure shapes in the Vesper build, one root each:

1. **The design arc failed by producing the HOW before the WHY** (iteration-log's own verdict) — already captured
   as process lessons in memory.
2. **The build arc failed by calling a partial pass DONE** — also mostly captured (slice-frame, verify-your-tools).
3. **The structural one — highest-leverage, NOT captured until this backlog:** *≈half of Vesper's systems were
   invented ad-hoc AFTER the pipeline declared the game "built."* `decisions_log[44]` says "THE GAME IS BUILT";
   then `[47]` cover, `[59]` capability, `[60]` yard-crawl, `[61]` coin economy, `[62]` reloads, `[71]` brothel,
   `[72]` loadout were all bolted on as off-pipeline Step-7 beats — and the design book carries **five** sections
   each tagged "— added during authoring." **The skill has no design step that asks "which genre subsystems does
   this game need?"** — so each was retrofitted into a locked structure with no story/blueprint/feedback pass.
   That's item **#1**, the umbrella over most of Group B.

---

## GROUP A — the structural headline

### 1. Systems grow through iteration — recipe menu + mid-stream fold-in loop ✅ DONE (2026-07-04)
`P1 (structural root) · effort M · skill · NEW system-patterns.md + run-mode.md, SKILL.md, step-2-toplevel.md, systems.md`
- **What Vesper taught:** ≈half of Vesper's systems (disguise, capability, coin economy, reload, loadout,
  day-depth) were invented ad-hoc AFTER the pipeline said "built." But — per LO — that's **not** a planning
  failure: sandbox systems legitimately EMERGE from play. The real problem was HOW they got folded in: jammed in
  raw as Step-7 beats, skipping the design passes, after the ledger had effectively said "done."
- **The reframe (LO's correction — the original "declare all systems on day one" framing was wrong):** NOT plan
  more upfront (that fights how design works). Instead — (a) a *reach-for-it* **recipe menu** you open when you
  feel a gap, and (b) a clean **mid-stream fold-in loop** + **"playable ≠ done"** so a discovered system gets real
  design passes instead of duct-tape.
- **Fix applied:** NEW `references/system-patterns.md` (7 starter recipes: disguise · capability · crawl · second
  economy · reload · loadout · day-depth). `run-mode.md` — NEW section "Systems grow through iteration — playable
  ≠ done" (the 4-pass loop: what/why/how-it-feels → place → build green → fold back). `SKILL.md` — operating rule
  "Structure is stable-and-extensible" extended from location/NPC/flag to whole systems + doctrine-library bullet.
  `step-2-toplevel.md §8` — reframed (declare engine toggles now; let authored subsystems emerge). `systems.md` —
  pointer distinguishing ENGINE toggles from these AUTHORED patterns.
- **Evidence:** `decisions_log[44,47,59,60,61,62,71,72]` · `design_book.md §1082/§1159/§1181/§1211/§1250`.

---

## GROUP B — new system doctrine the skill lacks (the categories #1 would surface)

> **Update (2026-07-04):** #1's new `system-patterns.md` menu now carries **starter recipes** for #2 (disguise),
> #3 (capability + crawl), #4 (second currency), #5 (reload upkeep), and #7 (loadout) — enough to build each right
> mid-stream. These items now mean *"deepen the starter recipe into a full standalone reference when a game leans
> hard on it,"* not *"nothing exists."* (#6 anonymous-venue is a `sex-loop.md` variant, not in the menu.)

### 2. Disguise / cover / identity-access clothing ⬜
`P1 · effort M · skill · clothing.md`
- Vesper's premise-central cover system (issued garment gates mission *entry*; wrong cover → wrong-reaction
  fallback beats) was reverse-engineered from `v2.py` and only formalized post-ship (`decisions_log[47]`).
- **Verified:** `clothing.md` is exposure-only (worn_corruption/exhibitionism); grep `disguise|cover|identity|
  infiltrat|undercover` across the whole skill = **0 hits**. **partial.**
- **Fix:** new section in `clothing.md` — "Clothing as an identity/access key": the `clothing_item` predicate
  gating a location *entry* / NPC first-contact door (not an escalation rung), + the wrong-cover fallback-beat
  pattern. Whole fantasy family (spy/honeypot/undercover) the skill currently can't build.

### 3. Capability / skill traits + stat-check crawl ⬜
`P1 · effort M · skill · NEW references/capability-ladders.md`
- Fighting/Stealth as trained traits, a training activity (diminishing curve + plateau + energy/time cost), the
  Burned-Yard depth-meter crawl (threshold gates + run fallback + depth-keyed finds), and the coupling rule "ship
  the READER in the same increment or the bar is the loudest dead meter" — all reasoned out live
  (`decisions_log[59,60,61]`; `design_book.md:1167-1177`).
- **Verified:** the non-corruption ladder exists only as a one-word design *question* (`content-framework.md:102`,
  `step-4-deep-design.md:48`). No pattern, no template. **partial.**
- **Fix:** new `capability-ladders.md` teaching the full drill→use→earn→spend loop + the crawl template; link from
  `content-framework.md §2D`, `step-4-deep-design.md §2D`, `step-5-blueprint.md`, `systems.md`.

### 4. Secondary / closed regional currency ⬜
`P1 · effort S · skill · step-2-toplevel.md`
- Vesper needed real coin (earn-there/spend-there, "worthless up top") with closed-loop discipline (every source
  balanced by a sink) and arm-at-first-relevance onboarding — all re-derived (`decisions_log[61,69]`).
- **Verified:** `step-2-toplevel.md:106` states "**One wallet** — money is money" as *law*; grep
  `second currenc|scrip|region-lock|closed-loop` = **0 hits.** **partial.**
- **Fix:** demote the one-wallet bullet from absolute law to default-with-named-exception; add "secondary currency
  (closed regional loop)" — earns its place only as a "second life" fantasy loop, sources balanced by sinks.

### 5. Consumable / ammo / reload upkeep loop ⬜
`P2 · effort M · skill · toml-gotchas.md, trait-catalog.md, systems.md`
- Two weapon charges (deplete-on-use, reload at a station) + the "keep upkeep loops SEPARATE — don't fold weapon
  reload into sleep" rule were built from verbal spec; the spend idiom came out inconsistent (costs vs effects by
  routing) (`decisions_log[62,72]`; `design_book.md:1250` "THREE SEPARATE upkeep systems").
- **Verified:** `systems.md:9-15` lists exactly 5 systems, no consumable row; `trait-catalog.md:130` defines only
  two trait categories. **partial.** Ties to #7 (clamp) and #1.
- **Fix:** generalize the spend idiom in `toml-gotchas.md §95` to "any spent resource incl. discrete consumable/
  ammo," give the one canonical deplete/reload shape, add the "upkeep loops stay separate" rule.

### 6. Anonymous / paid-service sex venue variant ⬜
`P2 · effort S · skill · sex-loop.md`
- The brothel needed the full pose-ladder loop for an anonymous john with no arc — pay-**on-finish** (not the
  entry faucet, a bug Vesper hit + fixed), upkeep drop on exit, cold register — copied by hand from Mercer
  (`decisions_log[71]`).
- **Verified:** `sex-loop.md:8-9` explicitly scopes the loop to "an NPC's full arc, not service/antagonist."
  **partial.**
- **Fix:** add a "Variant: anonymous/paid service venue (no NPC arc)" section (gate on access/coin/hygiene, no
  relation/corruption, pay-on-finish).

### 7. Loadout / carry-one-of-N = hidden integer trait ⬜
`P2 · effort S · engine · trait-catalog.md`
- A literal weapon slot is **engine-blocked** (`VALID_CLOTHING_SLOTS` hardcoded to 7, `template_import.py:158`);
  the right shape is one hidden integer trait (one value = mutual exclusion) + swap activity + trait gates, with
  auto-fire capstones gated on the TRIGGER so they wait instead of soft-locking (`decisions_log[72]`, commit
  `c91cad4`).
- **Verified:** the constraint is taught but only scoped to clothing coverage slots (`clothing.md:167`,
  `engine-reference.md:330`); the loadout *recipe* is in memory (`clothing_slots_hardcoded`) but **not the skill**.
  **partial.**
- **Fix:** promote the recipe into `trait-catalog.md` as "integer trait as an exclusive selector."

---

## GROUP C — resource & progression discipline

### 8. Clamp-or-the-HUD-card-VANISHES — hard lint ✅ DONE (2026-07-02)
`P0 · effort S · skill · beat-authoring.md, trait-catalog.md, step-6-feedback.md, toml-gotchas.md, engine-reference.md`
- **Shipped TWICE.** Any `op=add` on a banded body-stat without `clamp=true` lets it leave its bands; the card
  renders **blank** — a *missing* HUD element, not a wrong number. `decisions_log[64]` (Charge negative), `[66]`
  (hygiene over-cap AND negative — "SECOND time… a hard lint would kill the recurrence class — NOT actioned").
- **Fix applied:** the hard two-part rule (bound the value / cover the range) in `trait-catalog.md §4`; the §5
  cell made an active pointer; the bare-`+N` restore examples capped (`trait-catalog.md`, `toml-gotchas.md`);
  hard rows added to the Step-7 self-audit (`beat-authoring.md`) and the Step-6 review rubric
  (`step-6-feedback.md`); a pointer at the `engine-reference.md` Clamp trap. Reconciles the "corruption unbounded
  is correct" carve-out (completes it) instead of contradicting it; money stays exempt.
- *Engine truth verified:* `trait_words` closed-match `v2.py:15252`; `trait_status_text` open-on-omit `v2.py:15183`.

### 9. Grind-tuning / rung-pacing discipline ⬜
`P1 · effort M · skill · rts-design-philosophy.md, trait-design.md`
- The seduction climb broke on first play (rungs free + instant, thresholds bunched); the fix — a *diegetic* time
  cost that closes the NPC's schedule window (= a natural day-cap) + energy per rung + ~×2.5 threshold spacing —
  was retrofitted across ~25 sites (`decisions_log[58,161,176]`).
- **Verified:** the *principle* is taught (`rts-design-philosophy.md:72-77 P8`, `content-framework.md §5E`) but
  gives **no threshold-spacing guidance** and frames a removable daily-cap flag as sufficient (brittle). **partial.**
- **Fix:** replace the daily-cap-only framing with an explicit **throttle menu** (daily-cap flag / resource cost
  per rung / threshold spacing) + their trade-offs.

### 10. Day-BREADTH audit — "walk a representative day" ⬜
`P1 · effort M · skill · content-framework.md`
- Vesper's lean player thread made the vertical feeder-depth audit (§2E) *vacuously* pass, and Step 6 graded the
  ship "GO" — the day was "grind Renner + serve Mercer," and the thinness only surfaced when LO played it, forcing
  the entire post-ship day-depth rescue (`decisions_log[27,28,33]` → `[59]` "add things to DO per day").
- **Verified:** `content-framework.md:106 §2E` counts feeders *band-by-band* (vertical, one ladder); no horizontal
  count. **partial.** (Partially in memory `lane3_solo_schedule_redesign`.)
- **Fix:** add §2F "the day-breadth audit" after §2E — pick a representative mid-game day, list every *distinct*
  thing to do that is NOT advancing the single main grind; confirm at Step 6.

---

## GROUP D — the quest system

### 11. Design the Quests page as ONE system ⬜
`P1 · effort M · skill · beat-authoring.md`
- **Five** post-ship quest reworks (`decisions_log[54,55,57,65,73,75]`): no step designs the whole page (story-goal
  spine + per-NPC ladders + end-of-content card) up front. The stepped trait-band ladder (disjoint `gte X`+`lt Y`,
  one card live at a time, coaching in `goals[].label`) and the hard trap — *a MET numeric goal with no
  `ready_canvas` renders a BLANK sidebar next-row* (`v2.py:13988`) — were re-derived live.
- **Verified:** `beat-authoring.md:317-321` teaches only the FLAG-gated milestone chain; the ladder + trap live
  only in memory (`quest_card_ladder_and_renderer`). **partial.**
- **Fix:** add the "stepped trait-band ladder" pattern + the Frame-3-blank trap to `beat-authoring.md`; add a
  design-the-page-as-a-system pass.

---

## GROUP E — map / world

### 12. Complete `location-design.md` — aliveness calibration ⬜
`P1 · effort M · skill · location-design.md, step-2b-map-design.md`
- `location-design.md` was added this build, but its "cut any room with no content" hard-cut biases toward a
  lifeless scene-holder — the map LO **rejected** (`decisions_log[20]`, `iteration-log Loop 7`,
  `games/vesper/location_design_note.md`). "Earns its keep" must count *ambient life*, and the author should ask
  *how alive* the world should feel (Mode A) before drawing.
- **Verified:** `location-design.md:180-181` still hard-cuts atmospheric rooms; `§2:61-62` +
  `step-2b-map-design.md:31` still teach the rejected "add zones only where content lives." **partial (note never
  folded in).**
- **Fix:** add a Mode-A "how alive?" calibration before drawing the graph; reword the sizing rule to count ambient
  life, not just plot function; fold the game-folder note in + CHANGELOG it.

---

## GROUP F — design-coherence & writing-judgment doctrine

### 13. "What does the central institution DO?" + infiltration/cover coherence ⬜
`P1 · effort S · skill · content-framework.md`
- Two holes LO caught, not the author: the company's actual function was undefined after missions/tower/villain
  were built; and Renner-as-company-insider broke the honeypot (a man running the asset facility would *recognize*
  what she is) → recast to a deniable outside supplier (`iteration-log:124-129, 206-212`).
- **Verified:** `content-framework.md §1A:32-34` asks only the *player's* role; `§1E:62` checks only that the
  opening *lands* in prose. **missing.**
- **Fix:** add two §1 questions — (1) if the game hangs missions/factions/a villain off a named institution, what
  does it actually DO? (2) per infiltration target: can he see through the cover? If yes, the infiltration doesn't
  hold.

### 14. Restraint reflex — a character truth is a WRITING LENS, not a CONTENT GATE ⬜
`P1 · effort S · skill · kink-ceilings.md`
- ENI twice narrowed a hot beat to "cold help only" + kept a "but never I care about you" asterisk for character-
  purity; LO stopped it both times ("this is not a society-helpful game, we are building an adult porn game")
  (`transcript:4747-4797`, `iteration-log:187-199` + shortlist #7, `decisions_log[80]`).
- **Verified:** `kink-ceilings.md` governs *vocabulary crudeness* only (`:9-12`), never this reflex. **missing.**
- **Fix:** add an anti-pattern to `kink-ceilings.md §8` — using a character note to VETO/narrow a hot beat is a
  brake on the product; lead with the hot version, let the character truth color the *prose*, never the *content*.

### 15. Static / already-at-ceiling owner NPC arc shape ⬜
`P2 · effort M · skill · trait-design.md`
- Mercer (a pre-existing owner the PC already serves) has an open sex loop from scene one, no rungs, no climbing
  odometer, a flat hijack chance — improvised because every arc-shape row is a *climb*
  (`iteration-log:181-184`, `transcript:4041,4260`).
- **Verified:** `trait-design.md:35-41` arc-shape table = 5 climbing rows, no static/owner row. **missing.**
- **Fix:** add a 6th row — "Static / already-at-ceiling": spine = NONE, full loop live, no rungs, no climbing
  odometer, register shifts by pose/verb variety, no dead corruption meter.

### 16. Still-point player / two-axes-on-the-NPC model ⬜
`P2 · effort M · skill · step-2-toplevel.md, trait-design.md`
- The honeypot inverts the default: the player is the constant; BOTH progression axes live on the NPC doing
  *different* jobs (relation = ACCESS, corruption = SEDUCTION rungs, double-locked), and global player corruption is
  legitimately **dead** — re-derived over several turns (`transcript:2305, 6527`).
- **Verified:** `step-2-toplevel.md:32-34` + `trait-design.md:38` assume "player corruption = secondary floor."
  **partial/missing.** *(Corroborates memory `nonlinear_rpg_skill_research`: "the ONE critical gap = no
  player-identity axis — every player runs one monotonic corruption spine.")*
- **Fix:** name the still-point/infiltration player shape as a legitimate alternative to the corruption through-line.

---

## GROUP G — engine gotchas to fold into the skill (skill+engine)

### 17. QA-build vs deploy-build commands ⬜
`P1 · effort S · skill+engine · media.md, beat-authoring.md`
- `--debug` defaults to `./media` (so without `--video-folder` every clip 404s) AND bakes literal
  `[IMAGE MISSING] <path>` **text** into the HTML — a deploy build must **drop `--dev` and `--debug`** or stale
  placeholders/404s ship even after media is committed (memory `findmedia_nested_media_blindspot`).
- **Verified:** grep `--video-folder` across all skill files = **0 hits**; `beat-authoring.md:52-53,149` end the
  build cmd in `--dev`, no deploy variant. **partial.**
- **Fix:** add a "QA build vs deploy build" subsection to `media.md` + fix the build cmds in `beat-authoring.md`.

### 18. Milestone flag folded into a triggerless loop → build HARD-FAILS ⬜
`P1 · effort S · skill+engine · sex-loop.md, toml-gotchas.md`
- The flag-chain validator hard-fails ("MISSING HINT", `CommandError package_from_toml.py:364`) a flag required
  `is_true` by a downstream trigger/choice whose only setter is a triggerless canvas — fixed by re-expressing the
  milestone as a hidden trait counter (memory `flag_chain_validator_located_setter`).
- **Verified:** `sex-loop.md:26-29` teaches "state = numeric traits, never flags" for LOOP state only — and states
  the failure mode *wrong* ("reads ✗ NEVER SET"; actually the fatal is MISSING HINT). **partial + one wrong line.**
- **Fix:** correct rule #1 in `sex-loop.md` and teach the milestone-flag-in-loop case with the exact error text.

### 19. Container double-emit symptom ⬜
`P3 · effort S · skill · location-design.md`
- An `is_container` location with no `default_entry` double-emits its link (once in nav, once as a choice link),
  `v2.py:9079-9095` (memory `slice_frame_naivety`).
- **Verified:** `location-design.md:34` teaches only the container-*swallow* case. **partial.**
- **Fix:** add the double-emit symptom line to the container row.

---

## GROUP H — small doctrine / wording fixes

### 20. "Beat" is overloaded — design-beat (story chunk) vs build-node (screen) ⬜
`P2 · effort S · skill · beat-authoring.md`
- A design-beat is a story chunk; it explodes into MANY single-Continue nodes (opening = 3 beats → ~23 nodes). The
  "1 beat = 1 screen" framing caused a jargon detour (`iteration-log Loop 9`) and helped license collapsing the
  23-node opening to 3.
- **Verified:** `beat-authoring.md:4` "a beat is any story development" + `:46` "one beat per scene" vs
  `rts-flat-prose.md:55` prose-beat. Unreconciled overload. **partial.**
- **Fix:** add a 3-line reconciliation lifting Vesper's "design in beats, build in nodes."

### 21. Temporal dead-stat rule — don't introduce a core meter mid-game ⬜
`P2 · effort S · skill · step-2-toplevel.md`
- Lock the full meter set at Step 2; a meter that only pays off in Act 2 is a dead stat *now* (`iteration-log:129-130`,
  `decisions_log[50]`, `transcript:2305`).
- **Verified:** the dead-stat test (`step-2-toplevel.md:37-38`, `trait-design.md:150-158`) is *spatial* only.
  **partial.**
- **Fix:** add the temporal clause to the dead-stat test.

### 22. SKILL.md bare-asserts "(always-on)" ⬜
`P2 · effort S · skill · SKILL.md`
- The exact line that seeded the "is arousal always-on / does a machine get hormones" hallucination (Loop 2,
  `transcript:300-386`). Built-in traits are engine-*privileged* but NOT auto-initialized.
- **Verified:** `SKILL.md:93` says "(always-on)"; `trait-catalog.md:30` says the opposite ("a convention, not an
  engine constant"). Entry-point contradicts its own reference. **partial.**
- **Fix:** change `SKILL.md:93` to "(engine-privileged — still declare each)".

### 23. Pipeline one-liner omits Step 2b ⬜
`P3 · effort S · skill · SKILL.md`
- **Verified:** `SKILL.md:8` enumerates "fantasy → seed → top-level → casting → design → blueprint → feedback →
  authoring" — **drops map-design**, while the dispatch table `SKILL.md:40-49` lists `map_design` (2b). **partial
  (doc inconsistency, no build impact).**
- **Fix:** add map-design to the one-liner.

---

## GROUP I — process (framing implicated, mostly already captured)

### 24. Encode two process forcing-functions in run-mode ⬜
`P2/P3 · process · run-mode.md, SKILL.md`
- (a) Generalize propose-first to **all** planning-file writes, not just Step 5 — the "review surface = design
  book" framing (`SKILL.md:18`, `run-mode.md:67-72`) licensed the silent writes that alarmed LO. (b) Add a
  slice/ledger STOP — the abolished-slice doctrine has no enforcement.
- **Verified:** propose-first is explicit for Step 5 (`run-mode.md:83`); the general write-gate + the STOP aren't.
  **partial.** Both root lessons in memory (`lo_propose_before_writing`, `slice_frame_naivety`) — kept because the
  *skill framing itself* licensed the failure.

### 25. Pure process, already captured — NO skill edit ✅ (no action needed)
- AskUserQuestion-vs-pitches, gate-on-decisions, verify-your-tools, "story not a game." Each has a memory slug or
  doctrine home. Recorded for completeness only.

---

## FOLLOW-UP (discovered during #8)

### 26. `v2.py` citation-drift sweep after the engine renumber ⬜
`P2 · effort M · skill (fact-accuracy) · engine-reference.md + any file citing v2.py lines`
- The engine commits `8446b3d`/`1d9ce93` renumbered `v2.py`. `6b07567` already fixed the **slug/save** cites
  (`dev-console-jump.md`, `customization.md`, `SKILL.md`). But other line-cites likely drifted — e.g.
  `engine-reference.md`'s Clamp-trap cites (`eff.clamp || false` moved `1955/1872` → `1964/2047`; `_traitClamp`
  `5303-5306` → `5343/5398`; costs-clamp `4231` → elsewhere). A brittle line-cite that points at the wrong code is
  a silent hallucination.
- **Fix:** grep every `v2.py:<n>` / `template_import.py:<n>` cite across `references/` and re-verify against the
  current files; correct or convert to stable function-name anchors. (During #8 I already replaced the two cites I
  would have introduced with function-name references.)

---

## Shortlist — if you only touch a few

**Quick wins (P0/P1, effort S):** ✅ #8 (done) · #4 secondary currency · #13 institution-function · #14 restraint
reflex · #17 QA-vs-deploy build · #18 milestone-flag-in-loop · #22 "(always-on)" line.

**Big rocks (structural, effort M — the day-depth rescue you already paid for once):**
- **#1 the system-category checklist** (the umbrella — prevents the whole "invented after built" arc)
- #2 disguise/cover · #3 capability-ladders · #11 quest-page-as-a-system · #9 grind-tuning · #10 day-breadth ·
  #12 finish location-design aliveness

**Recommended next:** #1.

---

## Already fixed (verified — so we know they were checked, not skipped)
`media.md`, `onboarding.md`, `npc-intro.md`, `dev-console-jump.md`, `location-design.md` (created — but #12: still
incomplete on aliveness), `references/save-safety.md` (`6b07567`), content-framework §5G/§5H shared-space, the
day-system offscreen flag.

---

## Related open thread (outside the backlog)
**The `issue.md:6` save-compatibility question** — "do new releases break players' saved progress?" — is now
**largely answered** by the parallel engine work: constant slug IDs + a save-migration seam (`8446b3d`/`1d9ce93`)
plus the new `references/save-safety.md` doctrine (`6b07567`). Worth a read-through to confirm it covers what you
were worried about; the old "rebuild regenerates NPC UUIDs → stale save" failure mode should now be gone.
