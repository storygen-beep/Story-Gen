# Doc 38 — RTS Arousal System (comprehensive reference)

**Date:** 2026-05-21
**Subject:** How arousal works in *Road to Success* (RTS) — the player meter, the NPC meter, every source and sink, the cap behavior, and the live-verification record.
**Scope:** RTS only. No TLS comparison, no engine proposal — this is a pure mechanism reference.

**How this was derived.** Live-play session via the twine-game-explorer skill (slug `rts-arousal-deep`, URL `https://mopoga.com/road-to-success`). The arousal logic was extracted from the live 508 KB Story JavaScript (function bodies read directly), the 361-passage catalog was scanned for every `<<AddArousal>>` call site and arousal gate, and the load-bearing claims were verified at runtime — including a controlled sleep test that **caught and corrected a wrong first-pass assumption** (see §11). Everything below is grounded in source + runtime, not inference.

---

## 1. Executive summary (the key points)

- RTS has **two separate arousal meters**: one on **the player (Maya)**, scale **0–10**, and one on **each NPC**, scale **0–3** (the 🔥 / 🔥🔥 / 🔥🔥🔥 flames).
- **Both are no-decay, always-climbing meters.** They go up two ways — **+1 per relevant action** and **+1 automatically each new day** — and they **never fall over time**.
- **The only thing that lowers either is climax.** A sex scene's finish zeroes the player *and* the participating NPC in the same moment. Sleep does **not** reset arousal — sleep *raises* it.
- **The two meters do different jobs.** Player arousal is essentially an **on/off switch** (any value > 0 unlocks self-directed lewd actions; at 0 you can't even masturbate). NPC arousal is a **graded readiness ladder** — combined with that NPC's corruption, it gates how far a scene with him can go.
- **At max:** the player meter (10) is **cosmetic** — nothing in the game requires arousal above 1. The NPC meter (3) is **meaningful** — it's the requirement for that NPC's deepest sex stage, and the family NPCs reach it on their own via the daily rise.

---

## 2. The two axes

| | **Player arousal** | **NPC arousal** |
|---|---|---|
| Variable | `$player.arousal` | `$npc.<Name>.arousal` |
| Scale | `0 – $game.maxArousal` (= **10**) | `0 – 3` |
| Display | Bar widget + level label (Calm→Burning) | Flame label 🔥 / 🔥🔥 / 🔥🔥🔥 |
| Job | On/off gate for Maya's own lewd actions | Graded gate for that NPC's sex stages |
| Daily auto-rise | +1 every new day (always) | +1 every new day (**family NPCs only**, cap 3) |
| Action bump | +1 per lewd event done *to Maya* | +1 per tease aimed *at him* |
| Decay | none | none |
| Reset to 0 | only at climax (or explicit `ResetArousal`) | only at *his* climax |

They share nearly identical *rules*; they differ in cap, in what triggers the action bump, and in what they unlock.

---

## 3. Player arousal (Maya), 0–10

### 3.1 Display & level bands
The `ArousalDisplay` macro computes a 0–4 level from the raw value, then `LeftBarService.getArousalText` maps it to an icon + word:

```
arousalLevel = (arousal === 0) ? 0 : Math.min(Math.ceil(arousal / maxArousal * 4), 4)
```

| arousal | level | label | bar tint (fill width = arousal × 10%) |
|---|---|---|---|
| 0 | 0 | ❄️ Calm | low |
| 1–2 | 1 | 🔥 Warm | low |
| 3–5 | 2 | 🔥 Aroused | low → medium (>40% at a≥5) |
| 6–7 | 3 | 🔥 Hot | medium |
| 8–10 | 4 | 🔥 Burning | high (>70%) |

### 3.2 Sources (what raises it)
- **`<<AddArousal>>` → `StatsService.addArousal()` = +1, capped at 10**, fires an "Arousal increased" notification. There is **no parameterized add** for the player — every event emits the same +1.
- **38 `<<AddArousal>>` call sites across 28 passages**, by category:
  - **School:** Afterclass (×3), Cheerleader (×3), TeacherTutoring (×3), MathHomework (×2), ClassroomWidget.
  - **Flashing / exhibitionism:** LibraryExhibitionism (×2), GymFlash, MallFlash, BathroomFlashScene, BrotherBedroomFlash, CarWashChallenge, BeachChallenge1/BeachSwim, PoolSwim, ParkChallenge/ParkJog, StreetChallenge1.
  - **NPC tease / peep:** BedroomGrope (×2), PeepBrotherSex (×2), DadPeepSex, BrotherBedroomTease, DadBedroom, MarcusBathroomEncounter.
  - **Jobs / transit / misc:** RestaurantWork, PizzaDelivery, BusRandomEvent, ArtificialInsemination.
- **Drugs** write the field directly (bypassing the +1 mutator): `player.arousal = Math.max(0, player.arousal + mods.arousal)` — **Heroin = +8**, other drugs smaller.
- **New day / sleep = +1.** A full night runs `BedroomSleep → <<SleepCommon>> → <<NewDay>> → TimeService.newDay() → StatsService.resetPlayerStats()`, which does: energy → max, drunkenness → 0, and **`if (arousal < maxArousal) addArousal()`** (else pin at 10). You wake up *more* aroused. (A short **Nap** does not call newDay — arousal is untouched; verified live, §10.)

### 3.3 Sinks (what lowers it)
- **`<<ResetArousal>>` → `StatsService.resetArousal()` = set to 0.**
- **Climax** (`FinishSex`, §6) sets it to 0.
- **Nothing else.** There is **zero decay** — no `arousal--`, no `-=`, no `decreaseArousal` anywhere in the Story JS.

### 3.4 Read path & gallery
- Gates read via `getArousal()` = `galleryMode ? 10 : player.arousal`. Gallery/cheat mode reports max and short-circuits every mutator.

### 3.5 What it gates — the `>0` switch
- Of ~24 arousal gates in the passage set, **nearly all are `arousal > 0`** (a few `>= 1`); **none require a value above 1**.
- Canonical case: trying to masturbate at 0 is refused — *"You are not aroused enough to masturbate."* Arousal is **fuel an ambient event seeds into you**, which you then spend on bigger self-directed actions. You cannot bootstrap it from nothing.
- Consequence: the *height* of the player meter is essentially **flavor**. Mechanically only "above zero?" matters on the player side.

---

## 4. NPC arousal (the guy), 0–3

### 4.1 Data shape & display
`$npc.<Name>.arousal`, integer 0–3, shown as 🔥 / 🔥🔥 / 🔥🔥🔥. Read via `GetNpcArousal(npc)` (defaults to 0 if unset).

### 4.2 The daily auto-rise (the key mechanic)
Every new day, `TimeService.updateNPCs()` (called inside `newDay`) does, **unconditionally** and capped at 3:

```js
if (game().npc.Dad.arousal     < 3) game().npc.Dad.arousal++;
if (game().npc.Brother.arousal < 3) game().npc.Brother.arousal++;
if (game().npc.Grandpa.arousal < 3) game().npc.Grandpa.arousal++;
```

So the **family NPCs (Dad / Brother / Grandpa) get hornier on their own, +1 each morning, until maxed at 🔥🔥🔥** — no teasing required. The list is **hardcoded to those three by name**; other NPCs (e.g. Marcus) carry an `arousal` field but receive **no** daily bump.

### 4.3 Action bump
- Aimed teases use `increaseArousal(npc, 3)` (e.g. `<<AddBrotherArousal>>`, `<<AddDadArousal>>`): `npc.arousal = Math.min(npc.arousal + 1, 3)` — **+1 per tease, capped 3.**
- General events that arouse *Maya* do **not** raise the NPC; his meter rises only from the daily tick + teases directed at him.

### 4.4 Decay & reset
- **No decay**, no daily reset downward.
- Resets to **0 only when *he* climaxes** (the per-NPC reset inside `FinishSex`, §6).

### 4.5 `updateFamilyArousal()` is display-only
`CorruptionService.updateFamilyArousal()` re-renders the Dad/Brother/Grandpa arousal **labels** to match their current values. It does **not** propagate the player's arousal to NPCs. (This corrects a claim in the older `rts-arousal-sex-trace` notes that described it as propagation.)

---

## 5. Climax — `FinishSex` (the shared reset)

The scene-closing function ties everything together in one call:

```js
StatsService.addCorruption();          // player corruption +1
StatsService.resetArousal();           // player arousal → 0
if (npc === "Dad" || "Brother" || "Grandpa") {
    game().npc[npc].arousal = 0;       // that NPC arousal → 0
    NpcService.addCorruption(npc);     // that NPC corruption +1
}
if (inside) player().statistics.creampies++;   // + pregnancy roll if quest enabled
// + auto-tally of statistics (vaginal/blowjob/etc.) from the scene's flags
// + boyfriend logic: intimacy++ if he's the BF, else loyalty-- (cheating)
```

So a single orgasm **drains both meters at once** (player and the participating family NPC), advances both corruptions, and auto-updates the player's statistics counters from the scene's tagged flags — scene authors tag the scene, they don't write the stat code.

---

## 6. The stage-gate model (where NPC arousal does real work)

NPC arousal is the operative half of the scene-stage gates:

```js
StageOneCorruption(npc)   = galleryMode || (npc.corruption >= 5  && npc.arousal >= 1);
StageTwoCorruption(npc)   = galleryMode || (npc.corruption >= 10 && npc.arousal >= 2);
StageThreeCorruption(npc) = galleryMode || (npc.corruption >= 15 && npc.arousal >= 3);
```

Each escalation beat re-checks the NPC's arousal **and** corruption together. To reach a deeper beat with a specific NPC you must have raised *that NPC's* arousal (which, for the family, the daily tick does for you over a few days) and his corruption.

---

## 7. What happens at max

**Player at 10 (Burning) — cosmetic only.**
- No gate anywhere requires arousal above 1, so 10 unlocks nothing that 1 didn't.
- It cannot overflow — `addArousal` and the daily +1 both clamp at 10.
- It simply sits pinned at 10 until a climax drops it to 0. No forced event, no penalty, no bonus.

**NPC at 3 (🔥🔥🔥) — the green light.**
- 3 is the arousal requirement for `StageThreeCorruption` — the NPC's deepest sex stage (given corruption ≥ 15).
- The family NPCs reach 3 **passively** via the daily +1, so their top stage becomes available over time even without teasing.
- At 3 the daily tick stops incrementing (capped); it only drops when he climaxes.

---

## 8. Code anchors (Story JS, this build)

| Claim | Function / location |
|---|---|
| Player level math + bar tint | `Macro.add('ArousalDisplay')` (~L2188) |
| Level→label table | `LeftBarService.getArousalText` (~L5363) |
| Player +1 cap 10 + notification | `StatsService.addArousal` (~L8103) |
| Generic +1 cap helper | `StatsService.increaseArousal(npc, max)` (~L8098) |
| Player reset to 0 | `StatsService.resetArousal` (~L8189) |
| Sleep/new-day +1 (or pin at 10) | `StatsService.resetPlayerStats` (~L8143, esp. L8147–8148) |
| Drug arousal injection (Heroin +8) | `DrugService.applyDrugEffects` (~L7604) |
| Gallery override on read | `window.getArousal` (~L3020) |
| **Family daily auto-rise +1 cap 3** | `TimeService.updateNPCs` (~L10676–10681) |
| newDay → resetPlayerStats wiring | `TimeService.newDay` (~L10485) |
| Sleep passage → widget → NewDay | `BedroomSleep` passage + `SleepCommon` widget |
| Tease bumps (+1 cap 3) | `Macro.add('AddBrotherArousal' / 'AddDadArousal')` (~L3321 / L3359) |
| Per-NPC reset macros | `ResetBrotherArousal` / `ResetDadArousal` / `ResetGrandpaArousal` (~L3328+) |
| Shared climax reset | `FinishSex` closure (~L8062–8068) |
| Stage gates | `StageOne/Two/ThreeCorruption` (~L3008–3016) |
| Label refresh (not propagation) | `CorruptionService.updateFamilyArousal` (~L7458) |

*(Line numbers are from the concatenated Story JS of this build; treat as locators, not contracts.)*

---

## 9. Live-verification record

Session `rts-arousal-deep`, 2026-05-21.

- **Baseline reads:** `$game.maxArousal = 10`, fresh `$player.arousal = 0`, `$player.energy = 100`.
- **Nap (no new day):** set arousal = 4 → napped → arousal still **4**. Confirms naps don't touch arousal and there is no per-activity decay.
- **Sleep / new-day test** (the decisive one): set Maya arousal = 4, Brother arousal = 2, energy = 70; ran one new day via the game's own engine:

  | | before | after one new day |
  |---|---|---|
  | Maya arousal | 4 | **5** (+1) |
  | Brother arousal | 2 | **3** (+1, capped) |
  | energy | 70 | 100 (restored) |

  Confirms: sleep **raises** arousal on both sides (does not reset), and the family daily auto-rise is real.

---

## 10. Correction log

**First-pass error:** the initial analysis stated that NPC arousal *only* rises from teasing and that nothing changes it on a new day. This was **wrong**.

**How it was caught:** the live sleep test showed Brother's arousal moving 2→3 overnight with no tease involved. Tracing that to `TimeService.updateNPCs` revealed the hardcoded `if (arousal < 3) arousal++` daily bump for the three family NPCs.

**Lesson:** verify time/sleep/day-rollover behavior by **actually advancing a day in play**, not by reading the obvious mutators alone — passive per-day changes live in the time service, not in the arousal functions, and are easy to miss on a code-only read.

---

*Companion record: memory `rts_arousal_system.md` (condensed, already corrected). **RTS-vs-TLS comparison: doc 39.** Related RTS doctrine: doc 35 (state-variant + authored-vs-mechanism), docs 21–22 (RTS mechanism audits). Engine-feature work (a player-arousal primitive for our generator) is explicitly out of scope and deferred.*
