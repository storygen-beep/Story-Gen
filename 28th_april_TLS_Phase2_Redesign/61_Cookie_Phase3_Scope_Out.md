# Doc 61 — Cookie Phase 3+ Scope-Out Note

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Scope-out note — NOT a design brief. Formally documents Phase 3+ deferral.
**Supersedes:** nothing
**Sibling of:** Doc 58 (Ryan brief), Doc 59 (Jake brief), Doc 60 (Diana brief, blocked) — Cookie is the fourth in the slice-NPC quartet but does not get a brief in slice scope.
**Triggered by:** Doc 56 R7 / Doc 57 R7 require a design brief for every NPC before scaling authoring. Cookie has 2 shipped canvases (texture only) and Doc 30 §8.2 explicitly defers her arc to Phase 3+. This note formally documents the deferral so the R7 precondition is met by a scope-out rather than a real brief.

---

## §1 — Why scope-out instead of brief

**Doc 30 §8.2 (verified line 520):** *"Marge/Cookie — lesbian initiation — TBD (Phase 3+, deferred until those NPCs get authored)."*

**Doc 30 §4.2 fantasy commit (verified):** *"Workplace seduction + lesbian initiation; Marge is the dominant matriarch, Cookie is the peer fling."*

**Slice scope (verified per agent inventory):** Cookie is "peer voice texture, no arc" — line 543 of Doc 30 explicit. No fantasy committed in slice scope, no arc shape assigned, no stage trait, no ladder.

Writing a real design brief for Cookie now would either:
- (a) Manufacture an arc shape Doc 30 didn't commit (doctrine drift)
- (b) Restate Doc 30's deferral in brief form (overhead with no information gain)

This scope-out is option (c): formalize the deferral, document current shipped state, name the Phase 3+ trigger condition, satisfy R7 with a written record without manufacturing intent.

---

## §2 — Current shipped state (slice texture only)

| Canvas | Lane | Status | Notes |
|---|---|---|---|
| `scene_cookie_diner_evening` (line 9477) | L2 ambient | ✅ shipped | Off-shift encounter at diner. Peer-voice texture. Trust +1/+2 increments on Maya choices. No stage gates. |
| Diner-shift co-presence (inside `activity_diner_shift` and related, around line 9332) | Prose-only mention | ✅ shipped | Cookie is named in diner-shift activity prose as kitchen presence. Not her own canvas — she exists as setting detail. |
| `npc_cookie.trust` trait | Texture stat | ✅ tracked | Climbs via choices in scene_cookie_diner_evening. No gates currently consume it. |
| Quest cards | — | ❌ none | Cookie has 0 quest cards. Correctly excluded from quest roster per Doc 30 §4.2 (her arc is Phase 3+). |

**Diner-shift audit note (agent inventory §2.6):** "Cookie has zero canvases with `npc = 'npc_cookie'` trigger, so setup.getNpcLocation('npc_cookie') returns null." Scene_cookie_diner_evening was added later to fix NPC-location visibility for engine. This is a known engine-doctrine gap that doesn't affect slice play but matters for Doc 64 sidebar radar (Cookie's location wouldn't render unless a schedule is added or the scene_cookie_diner_evening counts).

---

## §3 — What slice scope KEEPS (no further authoring)

- **`scene_cookie_diner_evening`** stays as-is. Peer-voice texture, trust climbs, no arc gates. Working as designed.
- **Diner-shift co-presence prose** stays as-is. Cookie is named in the activity body; she's "there" in the scene's fiction without needing her own canvas to fire.
- **`npc_cookie.trust` trait** stays tracked. Even if no downstream gate consumes it in slice, the trait's persistence preserves Phase 3+ continuity — when Cookie's real brief lands, trust accumulated during slice play feeds Phase 3+ unlocks.

---

## §4 — What slice scope EXCLUDES (do not author)

- **Lane 1 hub** for Cookie. No "visit Cookie" affordance.
- **Lane 4 capstones** for Cookie. No first-time intro capstone, no stage transition canvases.
- **Cookie quest cards.** Slice roster stays at Frank R/R/R + Jake J1/J2/J3 + Marge M1-M5 + Ryan R1/R2/R3 + Story Goals (3-5) + Diana (0 per Doc 60).
- **Stage trait for Cookie.** Trust alone is sufficient for texture; no need for `npc_cookie_stage`.
- **Lesbian initiation content** of any tier. Doc 30 §4.2 commits the eventual fantasy but defers the authoring entirely.

**The constraint:** if a session is about to author Cookie content beyond the existing 1 ambient + texture prose, STOP. The R7 precondition is not met — this scope-out is not a brief; it's a deferral. To author Cookie content, first write a real brief replacing this scope-out.

---

## §5 — Doc 57 R7 compliance

Doc 56 R7 + Doc 57 R7 require *"NPC design brief declares arc shape + per-lane budget + vocab ceiling + tier flags BEFORE authoring begins."*

This scope-out IS the required compliance record. It formally states: **no further authoring for Cookie in slice scope.** Future Cookie work requires writing a real brief; this scope-out is its placeholder.

The R7 audit-checklist line for Cookie reads: *"design brief written" → "scope-out per Doc 61 — Phase 3+ deferred."*

---

## §6 — Phase 3+ trigger conditions

When does Cookie graduate from scope-out to needing a real brief? Any of these:

1. **Lesbian initiation arc greenlit.** Doc 30 §4.2 / §7.5 vocabulary commit. If LO opens lesbian content for the slice (or for Phase 2+/3+ proper), Cookie + Marge both need real briefs.
2. **Marge arc deepens past doctrine-locked service register.** Doc 53 commits Marge as a service NPC with 1-3 capstones. If Marge's arc extends into peer/sexual register (Phase 3+), Cookie's parallel arc unlocks simultaneously (per Doc 30 §4.2 — *"Marge is the dominant matriarch, Cookie is the peer fling"*).
3. **Diner becomes a Lane 1 NPC hub for Maya's seduction.** Currently diner is a workplace + activity. If Maya's diner activity becomes a corruption surface (workplace seduction), Cookie's role in those surfaces requires a brief.
4. **Cross-NPC arc transfer pattern adopted.** Doc 57 §10 mentions cross-NPC transfers (RTS `SellingMyStepsister`). If TLS opens that pattern, Marge → Cookie transfer is a natural candidate — requires both briefs.

**Until any of those land, this scope-out is the live record.**

---

## §7 — What the future Cookie brief will need to cover (forward-reference)

When Cookie's real brief lands (Doc 6X-Cookie-Brief), it should commit:

1. **Arc shape:** likely peer-with-workplace-context. Possibly a mini-quest-chain shape (Doc 13 §5 peer/quest-chain). Or service co-shape with Marge.
2. **Per-lane budget:** Doc 57 §5 has no row for "peer + workplace co-shape" — the brief will need to commit a budget. Likely small (3-6 canvases) given Cookie's peer role.
3. **Vocabulary ceiling:** Doc 30 §7.5 + LO's lesbian-content commit. Likely full ceiling at Phase 3+ ladder top.
4. **Tier flags:** stage trait or trust-only? Probably stage trait once arc opens. Need to define stages.
5. **Relationship to Marge's arc:** does Cookie come AS PART OF Marge's escalation, or as her own track? Both are possible per Doc 30 §4.2.

The future brief inherits this scope-out's "what's shipped" inventory as the starting state.

---

## §8 — References

### Sibling and ancestor docs

- **Doc 30** — TLS Test Redesign PRD (§4.2 fantasy "Cookie = peer fling," §5 NPC roster, §7.5 vocabulary ceiling deferred, §8.2 Phase 3+ deferral commit at line 520)
- **Doc 50** — Quest Card Shape Doctrine (Cookie correctly has 0 cards)
- **Doc 53** — Marge Redesign Brief (sibling NPC, currently in slice-clean service register; future lesbian arc couples)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (R7 brief precondition; this scope-out is the compliance record)
- **Doc 57** — Capstone Doctrine (R7 precondition same)
- **Doc 58** + **Doc 59** + **Doc 60** — sibling NPC briefs (Ryan, Jake, Diana)

### Live TLS reference

- `games/the_long_summer_test/toml_phases/7_final_game.toml:9477` — `scene_cookie_diner_evening`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:9332+` — diner-shift activity (Cookie as kitchen presence in prose)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:467+` — NPC declarations (Cookie at line ~546)

### Engine references

- `npc_cookie.trust` — texture trait; no gates consume it in slice
- `setup.getNpcLocation('npc_cookie')` returns null currently — known gap; addressable when real brief lands (add `[[npcs.schedules]]` entry or canvas with `npc = "npc_cookie"` trigger)
