# 27 — Frank 3-Lane Doctrine Remediation Plan

> **Status:** Ready to execute. Authored 2026-05-11.
> **Purpose:** Resolve the doctrine-drift issues identified in `26_Frank_3_Lane_Audit.md` — 7 issues across Lane 1 + Lane 2 + Lane 3, ordered by severity and dependency. Each issue gets: what's wrong, why it matters, concrete resolution approach, files to modify, effort estimate, dependency notes.
> **Source of issues:** `26_Frank_3_Lane_Audit.md` (3-lane audit completed same day)
> **Source of doctrine:** `21_RTS_Brother_Mechanism_Audit.md` + `22_RTS_Cross_NPC_Mechanism_Comparison.md` + `24_RTS_Three_Lanes_Repeatable_Activities.md`
> **Engine reference:** `25_Lane_3_Dispatcher_Substitution_PRD.md` (substitution mechanism)

## TL;DR

| Severity | Lane | Issues | Engine work? | Net effort |
|---|---|---|---|---|
| 🔴 CRITICAL | Lane 2 | L2-1 cascade conversion + L2-2 anti-toggle gate + L2-3 daily caps | L2-2 maybe (verify first) | 16-21 hr (top 6 cascades) |
| 🟡 MEDIUM | Lane 1 | L1-1 Pattern A render + L1-2 image pools + L1-3 Sleep-with-Frank + L1-4 Flash equivalent | L1-2 maybe (verify first) | 11-15 hr (top picks) |
| 🟢 LOW | Lane 3 | L3-1 1:N dispatcher + L3-2 Maya-bedroom | n/a — deferred | 0 hr |

**Total:** ~27-36 hr for full critical+medium remediation. Most edits land in `7_final_game.toml`.

**The "if you only have N hours" tier** (mirrors audit doc):

| Hours | Do | Net effect |
|---|---|---|
| 3 hr | L2-3 + L2-2 verify + L1-3 | Cooldown shipped + LN-band gap closed |
| 8 hr | + L1-4 + 3 cascades from L2-1 | Cooldown + 3 cascades + LN intimacy + Flash |
| 18 hr | All critical Lane 2 + L1-3 | **Biggest structural drift fixed** |
| 30 hr | All critical + medium | Full doctrine alignment |

---

## Execution discipline (added 2026-05-11 per user directive: "be very careful, go one by one")

Goal: zero regressions. Ship small atomic units that can be reverted independently. Never bundle unrelated changes.

### Per-issue protocol

**Pre-flight (before touching code):**
1. Re-verify the audit claim against current TOML — grep first to confirm the issue still applies. Audit data may be stale.
2. Re-read prior-pass memory for shipped patterns + trip hazards.
3. List specific lines that will change. If single issue >300 lines, split into sub-steps.
4. `git status` clean? Note any in-flight work touching the same files.

**Execute:**
5. ONE focused change per step. No "nearby cleanup" bundling.
6. Show planned edits as a list (slug + line number) BEFORE applying when multi-canvas.
7. Stop after diff lands. Don't continue until verification gates pass.

**Verify (ALL gates must pass):**
8. **Build clean** — `package_from_toml --dev`. No NEW warnings beyond pre-existing 8 overlap + 1 image-not-found.
9. **Pass 5 tests still green** — substitution test classes, 17/17.
10. **Live-play smoke test** of changed surface — daemon `--fresh` (avoid stale UUID), state-inject, verify fix lands.
11. **Regression sweep** — 3-5 unrelated surfaces (kitchen morning portrait + office hub + 1 Lane 2 random + 1 Lane 3 substitution).

**Document:**
12. Memory entry `frank_fix_<issue_id>.md` per fix.
13. MEMORY.md pointer.
14. NO commit until user approves.

### Check-in cadence

After each issue's verification gates pass: STOP. Show summary. Wait for user "go" before next issue. Do NOT auto-chain.

### Diff size discipline

Per-step cap: ~150 lines. Larger units split:
- L2-3 (15 canvases × 1 line each) ships in one step (15 lines total).
- L2-1 ships ONE cascade conversion per step (~100 lines each), not bundled.
- L2-2 Phase 2 splits: schema → parser → validator → engine eval → tests → TOML application (each its own sub-step).

### Common trip hazards (actively check)

- Stale daemon UUIDs after rebuild — always `--fresh`
- TOML uses slugs, runtime uses UUIDs — build resolves at emission
- `<<script>>` + `return` is illegal in SugarCube — use `<<set>> + <<if>> + <<goto>>`
- Hallway runtime passage is `Location_Home`, not `Location_Hallway`
- Locations declared in `7_final_game.toml`, not `1_metadata_and_locations.toml`
- Validator overlap-check excludes `substitution_only` canvases (Pass 6 fix)
- `previous()` predicate may not exist — verify FIRST before authoring engine changes (L2-2 Phase 1)

### Failure handling

Any verification gate fails → STOP. Investigate root cause. Don't paper over. If a regression is caught later, `git revert` the offending atomic commit.

---

## Context

The Frank → RTS-shape conversion shipped 7 passes (2026-05-11 → 2026-05-12). The 3-lane audit (doc 26) found:
- **Lane 1**: Partial doctrine match — Pattern E sex cascades ✅ + Pattern F refuse ✅, but rendered Pattern A tease/flash MISSING. Click-only doctrine drift.
- **Lane 2**: **Severe drift** — 0% cascade vs RTS's 81%. 15 single-render canvases where RTS uses linkreplace cascades. Wrong cooldown mechanism.
- **Lane 3**: Faithful — 100% cascade match + Pattern F refuse exceeds RTS. Effectively no remediation needed.

This doc resolves each issue lane-by-lane in severity order. The cascade primitive already ships (used in Lane 1 kitchen morning + capstones + Lane 3 substitutions); the substitution engine ships (PRD 25); the per-canvas daily cap mechanism ships (`max_triggers_per_day` per Pass 6 memory). Most issues are **content rewrites**, not engine work — except L2-2 (`previous()` gate) which needs an engine check first.

The intended outcome: Frank's three lanes deliver RTS-shape texture across the full daily routine, closing the doctrine gaps the audit identified, without rebuilding what already works (capstones, Lane 3, kitchen morning cascade).

---

## Issue inventory

| # | Lane | Issue | Severity | Engine work? | Effort |
|---|---|---|---|---|---|
| **L2-1** | 2 | Zero cascades across 15 ambient canvases | 🔴 CRITICAL | No | 12-16 hr (top 4-6) / 30-40 hr (full) |
| **L2-2** | 2 | No `previous()` gate (anti-toggle cooldown) | 🔴 CRITICAL | **Maybe** (verify first) | 3-4 hr |
| **L2-3** | 2 | No per-canvas `executedToday` daily cap | 🔴 CRITICAL | No | 30 min |
| **L1-1** | 1 | No rendered Pattern A tease/flash scenes | 🟡 MEDIUM | No | 6-8 hr (top 5) / 15-20 hr (all 11) |
| **L1-2** | 1 | No replay variety on tease items (image pool randomization) | 🟡 MEDIUM | Maybe | 1-2 hr engine + ~1 hr TOML |
| **L1-3** | 1 | No Sleep-with-Frank LN-band intimacy surface | 🟡 MEDIUM | No | 2-3 hr |
| **L1-4** | 1 | No Flash equivalent (exhibitionist register) | 🟡 MEDIUM | No | 1-2 hr |
| **L3-1** | 3 | 1:1 vs 1:N dispatcher economy | 🟢 LOW | No | Defer (only matters cross-NPC) |
| **L3-2** | 3 | No Maya-bedroom Lane 3 | 🟢 LOW | n/a | Defer (narratively-justified) |

---

## Resolution plan — issue by issue

### 🔴 Lane 2 issues (CRITICAL)

#### Issue L2-1 — Zero cascades across 15 ambient canvases

**What's wrong:** All 15 Frank Lane 2 canvases (`scene_kitchen_late_night_raid` / `scene_living_room_frank_radio` / `scene_porch_frank_evening_smoke` / etc.) ship as flat single-renders with `[group]` tier branching. Player walks into the kitchen, ~200-400 words of prose dump out at once. No click-paced reveal.

**Why it matters:** RTS Lane 2 is 81% cascade-bodied. The cascade is what makes Lane 2 "feel alive" — each click reveals next beat in real time, the scene develops as the player commits. TLS Frank's flat-prose Lane 2 reads as static texture; player has no pacing control over the encounter.

**Resolution approach:**

*Phase A — Pick the conversion targets (priority order)* — these are the 6 highest-impact Lane 2 canvases by current word count + dramatic register, ordered for max player-visible impact:

1. `scene_kitchen_late_night_raid` (328w, 2 tiers, deterministic chance=1.0) — N-band kitchen meet, doctrinally important
2. `scene_living_room_frank_radio` (410w, 5 tiers) — biggest canvas, richest prose, ideal cascade candidate
3. `scene_porch_frank_evening_smoke` (361w, 5 tiers) — Diana-down-the-hall risk register, escalation
4. `scene_back_porch_frank_weekend_morning` (352w Pass 4, 5 tiers) — weekend slowness, slow-cascade fits
5. `scene_kitchen_frank_coffee_alone` (217w, 3 tiers) — EM band, repeated daily
6. `scene_office_frank_diana_call_intercept` (81w, 0 tiers, one-time mutex) — Diana phone risk, dramatic moment

*Phase B — Per-canvas conversion process* (~2 hr per canvas):

For each canvas:

1. **Read current body**: identify the `[group]` tier branches and their per-tier prose
2. **Map to cascade structure**: per RTS Pattern D — SINGLE cascade with top-of-cascade flag-gated branches; low-stat path is 1-2 beats + rejection variant; high-stat path is 4-5 beats + climax. Per-tier register (pre-catch / post-catch / post-restrict / post-crack) preserved via cascade-level branching OR split-cascade pattern (one cascade per register).
3. **Rewrite body** using `type = "cascade"` block (existing primitive — see `frank_kitchen_morning_s0` at line ~2411 for canonical example):
   ```toml
   blocks = [
     { type = "cascade", props = { id = "frank_<scene>_<stage>", beats = [
       { blocks = [
         { type = "paragraph", content = "Beat 1 prose..." },
       ], advance_text = "Continue 👀" },
       { blocks = [
         { type = "paragraph", content = "Beat 2 prose..." },
       ], advance_text = "Click for next..." },
       # terminal beat: no advance_text
       { blocks = [
         { type = "paragraph", content = "Final beat prose..." },
       ] },
     ] } },
   ]
   ```
4. **Preserve effects**: existing single-render's stat ticks become per-beat effects (matches Pass 7 Frank cascade rollout pattern). Beat-level `effects = [...]` if a particular beat should fire a stat change (e.g., beat 2 fires Frank.arousal +1 because that's where his pen pauses).
5. **Add locked-sibling gates if appropriate**: if a beat shouldn't reveal at low Maya.corruption, use `show_when_locked` + `locked_text_threshold` (canonical: `scene_office_after_crack`).
6. **Preserve per-tier register branching**: convert top-level `[group]` tier branches into TIER-BRANCHED CASCADE props using cascade-level `gate` per beat OR split-cascade pattern (one cascade per register).

*Phase C — Verification per canvas* (~10 min):
- Build clean: `python manage.py package_from_toml --file games/the_long_summer_test/toml_phases/7_final_game.toml --dev`
- Live-play via twine-game-explorer: navigate to location at canvas's schedule, force-trigger via state injection, verify cascade reveals beat-by-beat (passage URL stable, body grows below cursor with each click)
- Verify per-tier prose still fires correctly (low Frank.trust + high Frank.trust + post-restrict capstone state)

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — body rewrite per canvas (~80-120 lines edited per canvas)

**No engine changes.** Cascade primitive already ships. Pass 6+7 verified the engine handles cascade emission + per-beat effects + locked siblings.

**Effort:** 12-16 hr for top 6 canvases. Full conversion of all 15 ≈ 30-40 hr.

**Phase D — Optional: convert remaining 9 canvases.** Lower-impact (shorter prose, fewer tiers) — ship in a later pass if first 6 prove the doctrine fix lands.

---

#### Issue L2-2 — No `previous()` gate (anti-toggle cooldown)

**What's wrong:** TLS Frank Lane 2 rolls chance% on every location entry — including re-entries from sub-passages. Player can exit a setter (e.g., Frank's office activity menu) → walk back to office → roll Lane 2 again. RTS prevents this via `<<if previous() == "Hallway">>` — Lane 2 only fires on FRESH hub entries, not sub-passage returns.

**Why it matters:** Player can exploit-spam Lane 2 by toggling sub-passages. Without this gate, the chance% values are misleading (effective fire rate is much higher than declared). Doc 24 §8.1's "RTS has no cooldown" claim is wrong — verified in audit.

**Resolution approach:**

*Phase 1 — Verify engine support (~30 min, READ-ONLY):*

Search the TLS engine for existing previous-passage checking:
- Read `apps/projects/services/template_import.py` around line 2684 (`triggerConditionsSatisfied` predicate vocabulary) — check if there's a `previous_passage` or `entry_from` predicate type
- Read `apps/game_generation/twee_comprehensive/generators/v1.py` around line 3919 (`checkRandomEncounters`) — see how the engine determines whether to roll
- Grep TLS for `previous()` or `entry_from` or `last_passage` usage

If a `previous_in` / `entry_from` predicate exists → skip to Phase 3.
If NO such predicate exists → Phase 2 (engine extension).

*Phase 2 — Engine extension (only if Phase 1 finds nothing, ~3-4 hr):*

1. **Schema addition** (`template_import.py:382`-area, `TemplateTrigger` dataclass):
   ```python
   # Lane 2 anti-toggle cooldown: only fire if entered from one of these locations.
   # Empty list = fire on any entry (default behavior).
   entry_from: List[str] = field(default_factory=list)
   ```
2. **Parser additions** (~10 lines following existing `chance` / `cooldown_message` parser pattern around line 964-1005)
3. **Engine eval** (`v1.py` `checkRandomEncounters` at line ~3919): before rolling chance, check if `setup.previousPassage` matches one of `entry_from`. SugarCube provides `previous()` — TLS engine should expose `setup.previousLocation` or equivalent. Wire it up.
4. **Validator** (`template_import.py validate()`): `entry_from` values must be valid location IDs.
5. **Test class**: 3-4 round-trip + emission tests in `apps/projects/tests.py`

*Phase 3 — TOML application (~30 min):*

For each of the 15 Lane 2 canvases:
- Add `entry_from = ["loc_hallway"]` (or whatever the parent hub is) to `[canvases.trigger]`
- Kitchen / living room / office / back porch / yard / bathroom: parent hub is `loc_hallway` (or `loc_back_porch` parent for some)
- Hallway: parent is the home root or `loc_property`

*Phase 4 — Verification:*
- Build clean
- Live-play: enter kitchen from hallway → Lane 2 fires. Click into a sub-passage (`activity_make_tea`), return to kitchen → Lane 2 should NOT re-roll. Confirmed via observed substitution skip on second entry.

**Files modified (Phase 2 path):**
- `apps/projects/services/template_import.py` — schema + parser + validator (~30 lines)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — engine eval (~15 lines)
- `apps/projects/tests.py` — new test class (~80 lines)
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — apply to 15 canvases (~30 lines)

**Effort:** ~4 hr if engine extension needed; ~30 min if predicate already exists.

**Tunable optional:** consider lowering the global Layer-3 cooldown (3-visit per-location) post-fix since `previous()` + per-canvas daily cap will provide pacing. Per doc 24 §8.1 this is a one-line change at `v1.py:3979` (`cooldowns[locKey] = 3` → 0 or per-canvas configurable).

---

#### Issue L2-3 — No per-canvas `executedToday` daily cap

**What's wrong:** Once a Frank Lane 2 ambient fires today, the SAME canvas can fire again the same day (subject only to global 3-visit cooldown). RTS's 44% of Lane 2 surfaces have explicit daily caps (`!$npc.X.scenes.SceneName.executedToday`). Once fired today, locked out.

**Why it matters:** Without daily caps, player can see the same Frank ambient twice in one day, breaking the "this is a moment" feel. Plus stat ticks accumulate beyond the doctrine's intent.

**Resolution approach:**

The TLS engine already supports per-canvas daily caps via `max_triggers_per_day` field (used by Pass 6 Lane 3 substitutions per memory). Pure TOML change.

For each of the 15 Lane 2 canvases, add to `[canvases.trigger]`:
```toml
max_triggers_per_day = 1
```

Exceptions:
- `scene_office_frank_diana_call_intercept` and `scene_hallway_frank_late_drink` already have one-time mutex flags (`frank_diana_call_intercept_used` / `frank_late_drink_used`) — stricter than daily cap, leave alone.

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 13 lines added (one per remaining canvas)

**No engine work.**

**Verification:** Build clean. Live-play: trigger Lane 2 at kitchen morning, advance time to next time band, return to kitchen morning the same in-game day. Same canvas should NOT re-fire. Different Lane 2 (afternoon canvas at different time band) IS allowed.

**Effort:** ~30 min.

---

### 🟡 Lane 1 issues (MEDIUM)

#### Issue L1-1 — No rendered Pattern A tease/flash scenes

**What's wrong:** Frank has ~11 click-only tease items distributed across hubs and ambient surfaces (office Pass-3 trio, kitchen brush past, hallway robe, radio rug, porch railing, dinprep plate reach, office supervised lean). Each is `targetType = "trigger"` — Maya clicks, stats tick, no scene renders. Player has zero narrative acknowledgement.

**Why it matters:** RTS Brother's Tease (69w + image pool of 5) and Flash (93w + image pool of 11) are the canonical Pattern A — short rendered passage with image + stat ticks + return. Player FEELS the show happened. TLS player only sees stat numbers move.

**Resolution approach:**

*Phase A — Pick promotion targets (priority order)*:

Top 5 to promote first (highest tease intensity + most-clickable surfaces):
1. Office "Lean over the desk to read the receipts" (Pass 3 office) — corr 5 first-tease beat
2. Office "Sit on the edge of the desk a moment" (Pass 3 office) — T2 escalation
3. Bedroom "Sit on the edge of his bed and wait" (Pass 3 bedroom) — corr 50 escalation
4. Kitchen "Brush past him at the coffee maker" (existing distribution) — most-frequent surface
5. Hallway "Linger in doorway in robe" (existing distribution) — exhibitionist register

The remaining 6 click-only items can be promoted in a later pass.

*Phase B — Per-item conversion (~1 hr per item)*:

For each click-only menu item:

1. **Author a new substitution_only canvas** at the same location (slug pattern: `tease_<location>_<action>`, e.g., `tease_office_lean_over_desk`)
2. **Body**: ~80 words rendered prose + 1 image block with `image_search_queries` (3-4 queries for image pool generation later) + per-tier branch on Maya.corruption (low-tier suggestive prose / high-tier overt prose)
3. **Stat effects on render**: Frank.arousal + Frank.corruption + Maya.corruption + energy (preserve existing effect deltas from the click-only version)
4. **Exit_block**: `type = "location"` returning to the parent location, +5-10 min time
5. **Update the source menu item**: change `targetType = "trigger"` → `targetType = "node"` + `nodeId = "tease_<location>_<action>.base"`. Drop the inline effects (now on the canvas).

This pattern reuses Pass 7's `scene_frank_at_open_bathroom_door` shape (T1 substitution_only canvas, single-image, brief prose, return-to-loc exit).

*Phase C — Verification (~5 min per item)*:
- Build clean
- Live-play: click each promoted item, verify rendered scene appears (passage URL changes), prose + image renders, stats apply on render, return-to-location works

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 5 new canvas entries (~80 lines each = ~400 lines) + 5 menu-item edits (~10 lines)

**No engine work.** Reuses `substitution_only` flag + image block + cascade-or-paragraph body — all primitives ship.

**Effort:** ~6-8 hr for top 5. Full set of 11 items = ~15-20 hr.

---

#### Issue L1-2 — No replay variety on tease items (image pool randomization)

**What's wrong:** Even when Pattern A scenes ship (per L1-1), they'll be identical every fire — same prose, same image. RTS uses `<<set $game.randomMedia to either("img1.webp", "img2.webp", ...)>>` to rotate among 5-11 images per scene per click.

**Why it matters:** Lane 1 Tease/Flash items can be clicked dozens of times in a playthrough. Without variety, the surface becomes visually monotonous. RTS rotates to keep replay interesting.

**Resolution approach:**

*Phase 1 — Verify engine support (~30 min, READ-ONLY):*

Search TLS image block schema:
- Read `apps/game_generation/twee_comprehensive/generators/v1.py` around the `image` block emission
- Check if image block supports an `images = [...]` array (multiple files) with random selection at render time
- Existing pattern: `image_search_queries` is a list (used by media pipeline) — but `file` is a single path

If multi-file random selection exists → use it.
If not → engine extension (Phase 2).

*Phase 2 — Engine extension (only if Phase 1 finds nothing, ~1-2 hr):*

Extend image block schema to support `files = ["path1.jpg", "path2.jpg", ...]` (list) in addition to `file = "path.jpg"` (single). At emission, pick randomly via SugarCube `<<set _img to either("path1.jpg", "path2.jpg", ...)>>`.

```python
# In v1.py image block emission:
if 'files' in props and len(props['files']) > 1:
    files_list = ', '.join(f'"{f}"' for f in props['files'])
    out += f'<<set _img to either({files_list})>>\n'
    out += f'<img src="@_img">\n'
elif 'file' in props:
    out += f'<img src="{props["file"]}">\n'
```

*Phase 3 — Apply to all promoted Pattern A scenes (~1 hr):*

For each Pattern A scene from L1-1, change image block from:
```toml
{ type = "image", props = { file = "tease/desk_lean.jpg", ... } }
```
to:
```toml
{ type = "image", props = { files = ["tease/desk_lean_1.jpg", "tease/desk_lean_2.jpg", "tease/desk_lean_3.jpg", "tease/desk_lean_4.jpg", "tease/desk_lean_5.jpg"], ... } }
```

Asset generation: 5 images per Pattern A scene × 5 scenes = 25 new images. Use existing media pipeline (per `nsfw_media_pipeline.md` references) or defer asset generation; engine + TOML changes work even with `_404.jpg` placeholders until media is generated.

*Phase 4 — Verification:*
- Build clean
- Live-play: click a Pattern A scene 10 times. Verify image varies; prose may stay consistent within a tier branch.

**Files modified:**
- `apps/game_generation/twee_comprehensive/generators/v1.py` — image block emitter (~10 lines)
- `apps/projects/services/template_import.py` — schema (image block validator allows `files` list)
- `apps/projects/tests.py` — 1 round-trip test
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 5 image block edits

**Effort:** ~2-3 hr engine + TOML. Asset generation deferred.

---

#### Issue L1-3 — No Sleep-with-Frank LN-band intimacy surface

**What's wrong:** Frank has bedroom hub access at Stage 4 (post-invitation), and a sex loop, and a first-night cascade. But there's no separate "fall asleep next to him" surface distinct from the sex loop. RTS reserves `SleepingBrother` (relation ≥ 10, LN-band only) as a relational + intimate beat — sleeping with him isn't sex.

**Why it matters:** RTS's late-game intimacy doctrine includes a relational beat that ISN'T sex. TLS Frank's LN-band content is sex-loop or nothing. Misses the doctrine slot for relational late-game intimacy.

**Resolution approach:**

Author one new canvas: `scene_frank_bedroom_sleep_overnight` — RTS Pattern D structure:

1. **Trigger**: location `loc_franks_bedroom`, schedule N-band 22:30-23:30 weekdays + LN band, conditions `frank_invited_to_bedroom is_true + frank_bedroom_first_done is_true + Frank.love gte 10`
2. **Add menu item to `scene_franks_bedroom_setter`**: "Sleep here tonight 💤" between "Get into bed" and "Goodnight". `show_when_locked = true` with locked_text_threshold "I'd want him to want me here for the night first — at least 10 love."
3. **Body**: 4-beat Pattern D cascade — Maya getting into bed (no undressing for sex), Frank's lamp going off, Maya turning toward him, his arm settling over her hip. ~150 words across beats.
4. **Effects on render**: +Frank.love (1-2), -Maya.calculation 1 (she's letting her guard down), +30 player.energy (full sleep), advances time to morning EM
5. **Exit_block**: `type = "choices"` — Pattern F-light fork (stay through morning vs leave before dawn). The existing first-night `scene_franks_bedroom_evening` already uses this fork pattern — copy structure.

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 1 new canvas (~120 lines) + 1 menu-item edit in setter (~15 lines)

**No engine work.**

**Verification:**
- Build clean
- Live-play: dev-shortcut to Stage 4 + Frank.love=15 + N band → enter bedroom → click Sleep here → cascade plays → effects apply → time advances to next morning. Verify clicking refuse path (leave before dawn) registers different stat changes.

**Effort:** ~2-3 hr.

---

#### Issue L1-4 — No Flash equivalent (exhibitionist register)

**What's wrong:** All 3 Pass-3 office tease items are same suggestive-proximity register (Lean / Stretch / Sit). RTS Brother has separate Tease (suggestive, 69w) AND Flash (explicit show, 93w) at the SAME corruption-5 threshold. Two flavors of self-display.

**Why it matters:** Authoring vocabulary missing the exhibitionist register means Frank Lane 1 covers half the player-agency self-display space. Player at corruption 5 has only "be subtly close" options, not "deliberately show him."

**Resolution approach:**

Add 1-2 Flash-equivalent rendered scenes (depends on L1-1 being done first since Flash is a Pattern A render):

**Option A — Bedroom Flash (Pass 3 bedroom expansion):**
- New canvas `tease_bedroom_robe_flash` (substitution_only Pattern A, ~90w)
- Menu item in `scene_franks_bedroom_setter`: "Open your robe a moment 👀" gated on Maya.corruption gte 5 (same threshold as RTS Flash)
- Body: Maya opens her robe a beat too long when crossing his bedroom doorway. Frank's eyes track. ~90 words. Single image (or pool per L1-2).
- Effects: Frank.arousal +2, Frank.corruption +1, Maya.corruption +1, player.calculation +1

**Option B — Bathroom Mirror Flash (using new bathroom location from Pass 7):**
- New canvas `tease_bathroom_mirror_show` (substitution_only Pattern A, ~80w)
- Reachable via bathroom Mirror activity exit choice (similar to Touch yourself in shower pattern)
- Body: Maya watches herself in the mirror, lifts her shirt. Frank passes the door (left open). Eye contact in mirror. ~80 words.
- Effects: Frank.arousal +2, Frank.corruption +1, Maya.corruption +1

Pick Option A as the canonical Flash equivalent (matches RTS bedroom-Flash location). Option B optional later.

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 1 new canvas (~100 lines) + 1 menu-item edit (~15 lines)

**No engine work** (assuming L1-1 ships first to establish the Pattern A render pattern).

**Effort:** ~1-2 hr.

---

### 🟢 Lane 3 issues (LOW — defer)

#### Issue L3-1 — 1:1 vs 1:N dispatcher economy

**What's wrong:** TLS uses 7 separate parent activities for 7 substitution targets. RTS uses 4 dispatchers — `BedroomStudy` alone rolls one dice for 4 NPC variants.

**Why it's deferred:** Only matters when adding Lane 3 for OTHER NPCs (Ryan/Jake) at the same activities. Frank-only scope means 1:1 is fine. The engine supports 1:N (just add multiple `[[canvases.trigger.substitutions]]` blocks to one parent) — author would just need to wire it.

**Resolution approach (when needed):** Future cross-NPC pass. Pick a parent activity with multiple plausible NPC walk-ins (e.g., `activity_wash_dishes_solo` could host both Frank-at-sink and a future Ryan-at-sink). Add a second `[[canvases.trigger.substitutions]]` rule.

**Effort:** ~30 min per dispatcher when activated. NOT in this plan.

---

#### Issue L3-2 — No Maya-bedroom Lane 3

**What's wrong:** RTS puts Lane 3 walk-ins in Maya's bedroom (Brother + Dad both arrive while Maya studies). TLS Frank doesn't visit Maya's bedroom.

**Why it's NOT a fix:** Narratively justified — Frank is Maya's stepfather; he doesn't enter her bedroom uninvited. The Lane 3 mechanism translates to shared spaces (kitchen, bathroom, living room, back porch) which Pass 6+7 already covered. **Accepted deviation, no remediation needed.**

---

## Suggested execution order

The strict dependency chain:

1. **L2-3** (per-canvas daily cap, 30 min) — no dependencies, smallest cost, biggest cooldown win
2. **L2-2 Phase 1** (engine verify, 30 min) — read-only, determines whether L2-2 needs engine work
3. **L2-2 Phase 2-3** (engine extension if needed + TOML application, 3-4 hr) — Lane 2 cooldown complete
4. **L1-3** (Sleep-with-Frank, 2-3 hr) — independent, closes LN-band gap
5. **L2-1 Phase A-C** (top 6 Lane 2 cascade conversions, 12-16 hr) — biggest player-visible improvement
6. **L1-1** (top 5 Pattern A promotions, 6-8 hr) — Lane 1 tease render
7. **L1-4** (Flash equivalent, 1-2 hr) — depends on L1-1 pattern
8. **L1-2** (image pool variety, 2-3 hr) — depends on L1-1 ship; engine work pending Phase 1 verify
9. **L2-1 Phase D** (remaining 9 Lane 2 conversions, 18-24 hr) — optional saturation pass
10. **L1-1 remainder** (6 more Pattern A promotions, 9-12 hr) — optional saturation pass

---

## Critical files

**Read-only references throughout:**
- `28th_april_TLS_Phase2_Redesign/26_Frank_3_Lane_Audit.md` — source of truth for issue definitions
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — RTS doctrine canonical
- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — Pattern A/D/E/F definitions
- `28th_april_TLS_Phase2_Redesign/25_Lane_3_Dispatcher_Substitution_PRD.md` — substitution engine spec
- `game_explorations/rts-arc-trace/passage_catalog.json` — RTS source for cascade reference

**Files modified:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — primary file (90% of edits land here)
- `apps/projects/services/template_import.py` — schema + validator (only L2-2 Phase 2 + L1-2 Phase 2)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — engine eval (only L2-2 Phase 2 + L1-2 Phase 2)
- `apps/projects/tests.py` — new test classes (only for engine extensions)

## Reusable primitives (already shipped)

- **Cascade block** — `type = "cascade"` with `props.beats[]` array. Canonical example: `frank_kitchen_morning_s0` at line ~2411 (Pass 7 rollout). Per-beat effects + locked siblings supported.
- **Substitution_only flag** — `substitution_only = true` excludes canvas from selectors. Canonical example: `scene_frank_at_open_bathroom_door` (Pass 7).
- **Cross-canvas nodeId routing** — `targetType = "node"` + `nodeId = "<slug>.<node_id>"`. Used throughout Pass 6+7.
- **Locked-sibling pattern** — `show_when_locked = true` + `locked_text` + `locked_text_threshold`. Used in office "Bend over the page" + bedroom "Undress for him".
- **Per-canvas daily cap** — `max_triggers_per_day = 1` on `[canvases.trigger]`. Used by Pass 6 Lane 3 substitutions.
- **Pattern F refuse path** — multi-node canvas with `node_climax` + `node_refuse`, exit_block `type = "choices"` forking to each. Canonical: `scene_office_after_crack` (Pass 7) + `scene_frank_walks_in_shower` (Pass 7).

## Verification

Per-issue verification documented inline in resolution approach. Aggregate verification:

1. **Build clean after each issue** — `python manage.py package_from_toml --file games/the_long_summer_test/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/the_long_summer_test/output --dev` — expect 🎉 Package ready, no NEW warnings.

2. **All Pass 5 substitution tests still green** — `pytest apps/projects/tests.py::SubstitutionsRoundTripTests apps/projects/tests.py::SubstitutionsValidatorTests apps/projects/tests.py::SubstitutionsEngineEmissionTests`. 17/17 pass.

3. **Live-play via twine-game-explorer per fix-pass:**
   - Build, restart daemon `--fresh` (avoid stale UUID per Pass 6 trip hazard)
   - Inject state for the relevant Frank stage / corruption / location
   - Click through the changed surface and verify: cascade reveals beat-by-beat (L2-1) / Lane 2 doesn't re-roll on sub-passage return (L2-2) / canvas locked out same day (L2-3) / Pattern A scene renders (L1-1) / image varies per click (L1-2) / Sleep-with-Frank cascade fires (L1-3) / Flash item renders (L1-4)

4. **Regression sweep after major fix-passes** — re-test Pass 1 / 3 / 4 / 6 / 7 surfaces still work: kitchen morning portrait + office hub menu + Lane 2 ambient (post-cascade-conversion) + Lane 3 substitutions + bathroom shower walk-in.

5. **Doc 24 §8.1 should be revised** post-L2-2 ship — the "RTS has no cooldown" claim is wrong per audit, and the TLS-vs-RTS cooldown comparison gets flipped after this remediation. One-paragraph correction at the end of doc 24 §8.1.

## What this plan deliberately does NOT cover

- **Cross-NPC remediation (Ryan / Jake / Diana)** — Frank-only scope per audit. Same patterns will apply to those NPCs in their own conversion passes.
- **Lane 3 minor issues (L3-1 + L3-2)** — deferred per audit. L3-1 only matters cross-NPC; L3-2 is narratively-justified deviation.
- **Asset generation** (L1-2 image pools) — TOML + engine changes work with placeholder paths; image generation is downstream media-pipeline work.
- **Full Lane 2 saturation** (remaining 9 canvases of 15 after top 6 done) — optional later pass; biggest impact lands in top 6.
- **Full Lane 1 saturation** (remaining 6 of 11 click-only items after top 5 done) — same.
- **New mechanics not in audit** — e.g., NotifyCorruption-equivalent threshold messages (mentioned in audit candidate-fixes but NOT a doctrine-required gap; deferred).

---

End of doc.
