# Doc 41 — Low-Arousal Gating Completeness PRD (RTS-faithful)

**Date:** 2026-05-21
**Builds on:** doc 38 (RTS Arousal System), doc 40 (Player Arousal Engine PRD — shipped).
**Status:** ✅ Tier 1 SHIPPED 2026-05-21. Gate A (`player arousal gte 1` on all 10 sex-loop entry choices) + Gate B (`npc_frank arousal gte 1` on all 8 `ambient_*_frank_*` ambients) implemented in `7_final_game.toml`; build clean (no new warnings); browser live-play GREEN (A false@0/true@1, B false@0/true@1, teases ungated → no soft-lock). **Gate C resolved without pose-menu changes:** the in-loop climax is already gated by `loop_npc_pleasure gte 50` (in-scene arousal that builds as you act), so the cum-bearing choices are strand-free without bolting Frank's 0–3 trait onto poses — see §5 note. Memory: `tls_player_arousal.md`. (Original PRD text retained below.)

**Problem.** Doc 40 made TLS arousal *accumulate / cap / never decay / reset at climax* exactly like RTS, and wired the two canonical gates (shower self-act `arousal gte 1`; Frank shower walk-in `arousal gte 3`). But RTS gates **low arousal pervasively**, and TLS does not — so at low/zero arousal TLS still lets through content RTS would lock. This PRD closes that gap.

---

## 1. The RTS gating model (source-verified)

From `game_explorations/rts-arousal-deep/passage_catalog.json`. RTS uses **three distinct arousal gates**, each for a different actor:

### Gate A — player self-act: `getArousal() > 0` (≈14 sites)
Wraps Maya's OWN sexual actions. Verified pattern:
```
<<if getArousal() > 0>>
    <<goto "BedroomMasturbate">>
<<else>>
    <<Notification 'warning' "You are not aroused enough to masturbate">>
<</if>>
```
Applied to: masturbation in 4 locations (`ApartmentBedroom`, `SchoolBathroomCabin`, `BathroomShower`, `Bedroom`); the "you start touching yourself" escalation beat inside peep scenes (`PeepBrotherSex`, `DadPeepSex`); player-led sex initiation (`BrotherBedroom`, `MarcusBedroom` — `<<if getArousal()>0>> <<goto …Sex>>`); the webcam activity (`Laptop` — `<<if $player.arousal < 1>>` shows 🔒 Locked). Pure on/off — any value > 0 unlocks; magnitude is flavor.

### Gate B — NPC "in the mood": `npc.arousal > 0`
Gates whether NPC-INITIATED ambient events fire. Verified pattern:
```
<<if random(1,3) == 1 && $npc.Dad.arousal > 0 && IsNpcAtHome("Dad")>>
    <<goto "EatSex">>
<</if>>
```
Used in `BedroomGrope`, `KitchenEat`, `WashDishes`. The inverse appears in `GrandpaBedroom`: `<<if $npc.Grandpa.arousal == 0>> Notification "He isn't in the mood right now…"` — visiting a cold NPC makes him decline.

### Gate C — graded NPC ladder: `StageOne/Two/ThreeCorruption(npc)`
`= npc.corruption ≥ 5/10/15 AND npc.arousal ≥ 1/2/3`. Used 17 passages (StageOne 6×, StageTwo 14×, StageThree 7×). Gates each DEEPER beat inside a sex-scene cascade — e.g. `BrotherShowerSex` checks `StageTwoCorruption($npc.Brother)` to reveal the mid beat, `StageThreeCorruption` for the finale.

---

## 2. Doctrine — gate the ACTS, not the teases

RTS gates **masturbation, sex initiation, and deeper beats** on arousal. It does **NOT** gate teases/flashing — those are the *seeders* that RAISE arousal. This is load-bearing: if you gated the seeders on arousal too, the loop would **deadlock at 0** (nothing could lift you off the floor). The seeders must stay open so a Calm Maya always has a way to warm up. Our daily `+1` and the per-beat `+1` reinforce this, but the ungated teases are the deliberate escape hatch.

---

## 3. TLS gap → fix (content-only)

| Gate | RTS | TLS today | Fix |
|---|---|---|---|
| **A** player self-act | masturbation + player-led sex init gated `>0` | only shower "Touch yourself" (`gte 1`) | Add `player arousal gte 1` to the **`loop_franks_bedroom_sex` entry** choices (the "Have sex with him" / undress-for-him initiations). Keep the 6 `tease_*` canvases UNGATED. |
| **B** NPC in-the-mood | ambient events gated on his `arousal>0` | 13 Lane-2 `trigger_mode="random"` Frank ambients fire on chance%+schedule only | Add `{ subject:"npc", npc_id:"npc_frank", trait_key:"arousal", operator:"gte", value:1 }` to each of the 13 ambient trigger condition blocks. |
| **C** graded ladder | every escalation beat re-checks `corruption≥X AND arousal≥Y` (1/2/3) | only the shower walk-in (`arousal gte 3`) | Tier the `loop_franks_bedroom_sex` rungs: pair the existing corruption/`sex_stage` gates with `npc_frank arousal gte 1 / 2 / 3` (kiss/oral→1, mid→2, penetration/finish→3). |

**Target inventory** (from this session's survey of `7_final_game.toml`):
- Gate A: the entry choices on `loop_franks_bedroom_sex` (id at ~L3284). Untouched: `tease_hallway_robe_linger`, `tease_bedroom_robe_flash`, `tease_bedroom_hand_near_his`, `tease_kitchen_general`, `tease_livingroom_general`, `tease_yard_general`.
- Gate B: the 13 `trigger_mode = "random"` ambient canvases (the kitchen/living-room/yard/hallway Frank Lane-2 set).
- Gate C: the escalation rungs inside `loop_franks_bedroom_sex` (and its finisher entry).

All fixes are additive condition items on existing AND blocks — no new schema, no engine work.

---

## 4. Anti-soft-lock check

At Maya arousal 0 on a fresh day, can she still get aroused? **Yes:**
- The 6 teases are ungated → she can always display/flirt to seed arousal.
- The daily `+1` (and sleep) lifts her off 0 each new day.
- Every Frank lewd beat grants player `+1` (doc 40).

The Gate-A/B/C additions only block the *acts* (masturbate, initiate sex, deeper rungs, NPC-initiated events) — never the seeders. So there is no state from which arousal cannot rise. Gate B uses `npc_frank arousal gte 1`; Frank's `+1/day` keeps him "in the mood" most days, so it rarely suppresses — it's structurally faithful, not a content choke.

---

## 5. Effort / risk tiers

- **Tier 1 — A + B (recommended first):** clean, bounded, low risk. Add `player arousal gte 1` to the sex-loop entry; add `npc_frank arousal gte 1` to 13 ambient triggers. Pure additive gates.
- **Tier 2 — C (graded ladder):** deeper authoring; re-tunes when penetration/finish unlock (now also requires Frank arousal 2/3, not just corruption/`sex_stage`). Medium risk — verify it doesn't strand the loop mid-escalation when Frank is under-aroused. Ship after Tier 1 is live-verified.

---

## 6. Verification plan (for the eventual implementation)

1. **Build:** `package_from_toml` clean, no NEW warnings.
2. **Live-play (twine-game-explorer on the local build):**
   - At Maya arousal 0: sex-loop entry **blocked** ("not aroused enough"); the teases still **work** (and raise arousal).
   - Set Frank arousal 0: his Lane-2 ambients **do not fire**; raise to ≥1: they fire again.
   - Gate C: with Frank arousal 1 only the early rungs show; at 2 the mid rung; at 3 the penetration/finish rung.
   - Confirm a fresh arousal-0 start is NOT soft-locked (teases + daily rise lift it).
3. Mirror canonical bits to phase files; regenerate `output/`; memory + doc-41-shipped note.

---

## 7. Critical files (implementation, not this PRD task)
- `games/the_long_summer_test/toml_phases/7_final_game.toml` (build input): `loop_franks_bedroom_sex` entry + rungs (~L3284), 13 random-trigger ambient blocks. Mirror to phase files per the doc-40 / clothing precedent.
- All gates reuse the existing condition primitive (`triggerConditionsSatisfied`, trait/subject/operator) — confirmed working in docs 37/40.

---

*Companion: docs 38 (RTS arousal) / 40 (player arousal, shipped). Memory: `tls_player_arousal.md`, `rts_arousal_system.md`. Recommend implementing Tier 1 first.*
