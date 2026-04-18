# Static health — road-to-success

Generated: 2026-04-17T16:06:27.930Z

## Verdict: ❌ FAIL

| Metric | Value | Bar | Result |
|---|---|---|---|
| definite_ambiguous_rate | 0.0% | ≤ 5.0% | ✅ |
| potential_ambiguous_rate | 2.7% | ≤ 20.0% | ✅ |
| dynamic_goto_rate | 1.1% | ≤ 10.0% | ✅ |
| effective_gate_unknown_rate | 52.0% | ≤ 30.0% | ❌ |
| complex_setter_density | 0.9% | < 5.0% | ✅ |

## 1. Click-text ambiguity

Edges bucketed by (source_passage, click_text). Raw duplicate buckets (≥2 edges sharing the key): **27**. Most of these are expanded `<<if>>/<<elseif>>` chains where only one gate fires at a time — not a real runtime ambiguity.

**Definite ambiguous** (≥2 edges in the bucket evaluate to `true` on initial state — autopilot *cannot* disambiguate):
- 0 / 372 edges (0.0%)

**Potential ambiguous** (bucket has ≥2 edges with gates that could fire concurrently at runtime — typically due to temp vars / runtime-computed state the evaluator flags as `unknown`):
- 10 / 372 edges (2.7%)

**Top offenders:**
- `ThomasParty` → "Go to your house 🏠" × 2 (gates: 0 true, 2 unknown, 0 false)
- `ApartmentSleep` → "Wake up" × 2 (gates: 0 true, 2 unknown, 0 false)
- `SleepingBrother` → "Go to your bedroom and sleep 😴" × 2 (gates: 0 true, 2 unknown, 0 false)
- `Laptop` → "Shutdown 🔴" × 2 (gates: 0 true, 2 unknown, 0 false)
- `NoEnergy` → "Go to your house" × 2 (gates: 0 true, 2 unknown, 0 false)

## 2. Dynamic-goto coverage gap

- 4 / 358 passages contain `<<goto $var>>` or similar (1.1%)

**Sample passages:**
- `SchoolBathroomCabin` → `<<goto $bathroom>>`
- `DevWidget` → `<<goto _devLocation>>`
- `LightningKidnapping` → `<<goto $game.lastPassage>>`
- `Thief` → `<<goto $game.lastPassage>>`

## 3. Gate-eval on initial state

- 333 edges have non-empty gate stack
- true: 12 | false: 132 | unknown: 189
- raw unknown rate: 56.8%

**Unknown breakdown by gate variable class:**
- temp-var-only (`_var` — resolves at runtime): 16
- story-var-only (`$var` — real evaluator gap): 30
- mixed: 143

**Effective unknown rate** (temp-only gates excluded since they resolve at runtime when the current passage is being rendered): 52.0%

**Sample story-var unknown gates** (these are the real evaluator gaps — autopilot will see `unknown` here even at runtime):
- `BarDrink` → `VeronicaMeet` (click: "Veronica's House") — [if] getCorruptionLevel() >= 3 && getDrunkness() == 3 ∧ [if] $player.trans && $npc.Veronica.relation == 0
- `BeachNight` → `Beach` (click: "null") — [if] $game.time == "N" == false && $game.time == "LN" == false && $game.time == "E" == false
- `ClubDance` → `JamalMeet` (click: "Go with him") — [if] random(1,2) == 1 ∧ [if] getCorruptionLevel() >= 2 ∧ [if] checkSceneReq("ClubFlash") ∧ [if] random(1,2) == 1 && $npc.Jamal.scenes.JamalMeet.unlocked == false
- `ClubDance` → `Club` (click: "No, thanks") — [if] random(1,2) == 1 ∧ [if] getCorruptionLevel() >= 2 ∧ [if] checkSceneReq("ClubFlash") ∧ [if] random(1,2) == 1 && $npc.Jamal.scenes.JamalMeet.unlocked == false
- `OfficeInterview` → `Office` (click: "Leave the office") — [if] galleryMode() || $player.intelligence >= 10 ∧ [if] !galleryMode()
- `OfficeInterview` → `Office` (click: "Leave the office") — [if] galleryMode() || $player.intelligence >= 10 ∧ [if] !galleryMode()
- `OfficeInterview` → `Office` (click: "Leave the room") — [if] galleryMode() || $player.intelligence >= 10 ∧ [if] getCorruptionLevel() >= 3 ∧ [if] !galleryMode()
- `OfficeInterview` → `Office` (click: "Leave the room") — [else] !(galleryMode() || $player.intelligence >= 10)
- `PoolSwim` → `PoolSwimSex` (click: "Kiss him 👄") — [if] random(1,3) == 1 || $player.clothing.corruption >= 30 ∧ [if] getExb() >= 10 ∧ [if] checkSceneReq("PoolFlash") ∧ [if] getExb() >= 15 ∧ [if] getCorruptionLevel() >= 3 ∧ [if] checkSceneReq("PoolSwimSex")
- `ThomasParty2Floor` → `ThomasPartySpinTheBottle` (click: "Play") — [if] random(1,3) == 1 && $location.thomasHouse.scenes.ThomasPartySpinTheBottle.executedToday == false ∧ [if] getCorruptionLevel() >= 3 || getDrunkness() >= 3

## 4. Complex setters

- total variables: 132
- parsed setters: 563
- complex (unparseable) setters: 5
- parse errors: 5
- skipped script blocks: 22
- skipped widget passages: 13
- complex setter density: 0.9%
- indexing coverage: `partial`
