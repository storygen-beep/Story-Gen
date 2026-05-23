# Doc 39 — RTS vs TLS Arousal (comparison)

**Date:** 2026-05-21
**Subject:** How arousal in *Road to Success* (RTS) differs from arousal in The Long Summer (TLS) — mechanics, behavior, and design philosophy.
**Companion to:** doc 38 (RTS Arousal System, the full RTS reference). This doc assumes doc 38 for the RTS side and focuses on the contrast.

**How each side was verified.** RTS — live-play + Story-JS extraction (doc 38, slug `rts-arousal-deep`). TLS — read directly from `games/the_long_summer_test/toml_phases/7_final_game.toml` and the engine generators (`apps/game_generation/twee_comprehensive/generators/v2.py`).

---

## 1. Executive summary

The two games use the same *word* for almost opposite things.

- **RTS arousal is a two-axis, player-centred fuel economy that only ever climbs.** Maya has her own 0–10 meter; each guy has his own 0–3 meter; both rise from actions and rise again every day, never decay, and reset only at climax.
- **TLS arousal is a single decaying NPC mood-trait that gates one scene.** Only the NPCs (Frank/Jake/Ryan) have it; **Maya has no arousal at all**. It is a generic 0–100 trait that the author pushes up or down with effects, and the engine quietly bleeds it back down ~1/day if you neglect that NPC.

One accumulates; the other evaporates. That is the whole story in a sentence.

---

## 2. Side by side

| | **RTS** | **TLS** |
|---|---|---|
| **Whose stat** | Player **and** NPC (two separate axes) | **NPC only** — Maya has none |
| **Scale** | Maya `0–10`; each guy `0–3` | `0–100` per NPC (bands: calm/aware/yearning/burning) |
| **What moves it up** | +1 per action **and** +1 every new day, automatic | Authored tease effects (+1/+2/+5). No automatic gain |
| **What moves it down** | Climax only (→0) | Per-day decay (~1) **plus** authored drops (−2 frustrated, −3 spent) |
| **Direction over time** | **Always climbs** (no decay; sleep adds +1) | **Fades** if the NPC is ignored (use-it-or-lose-it) |
| **What it gates** | Maya: `>0` switch on her own lewd acts; NPC: 0–3 stage ladder | **One** scene (Frank shower walk-in needs arousal ≥30) |
| **Is it "fuel"?** | Yes — can't act at 0; seed it, then spend it | No fuel concept; arousal only tracks *his* state |
| **Implementation** | Engine-coded subsystem (macros, caps, daily-rise, bar UI, gallery freeze) | Generic `core_trait` moved by declarative effects; decay is the only engine-added behavior |

---

## 3. The three differences that matter

**(a) There is no player arousal in TLS.** RTS's whole loop is *Maya gets turned on → spends that arousal on lewd actions*. TLS dropped that axis entirely — arousal is exclusively "how worked-up is the NPC." Maya's desire is carried by `corruption` and narrative, not a meter. This is the single biggest divergence.

**(b) Decay flips the pressure direction.** RTS arousal is a ratchet — it climbs from actions, climbs again each morning (sleep raises it), and never falls until you climax. You can bank heat indefinitely. TLS arousal **bleeds back ~1/day if you don't engage that NPC** (the engine skips the decay only on days you interacted with him). So RTS rewards *letting tension accumulate*; TLS pressures you to *keep the NPC warm* or his gated content drifts out of reach.

**(c) TLS borrowed the NPC-arousal-as-stage-gate idea — but used it exactly once.** RTS's deepest beat needs `npc.corruption ≥ 15 AND npc.arousal ≥ 3`. The TLS Frank-shower walk-in copies that shape verbatim — `Frank corruption ≥ 10 AND Frank arousal ≥ 30` (plus player corruption ≥ 20). So the doctrine *is* present in TLS, just as a single application rather than RTS's systemic ladder where every escalation re-checks NPC arousal.

---

## 4. A real "system" vs a plain trait

Underneath, both are just integer fields. The difference is what surrounds the integer.

- **RTS** fronts the number with **dedicated JavaScript that enforces rules**: fixed +1 steps (`addArousal`), hard caps (10 / 3), the daily auto-rise (`updateNPCs`), the climax reset (`FinishSex`), the bar widget + level math, and a gallery-mode override. The mechanics live in **engine code**.
- **TLS** has **no arousal-specific code at all**. Arousal rides the *generic* effect pipeline — the same `{op:"add", value:N}` machinery that moves money, energy, love, and corruption — and the *generic* emotion-range display. The only engine behavior layered specifically onto it is the per-day decay (one config line, `[npcs.trait_decay] arousal = 1.0`). The mechanics live in **authored content**.

Same data, opposite philosophies: **RTS encodes the rules in the engine; TLS leaves the number naked and lets the content author be the rules.**

---

## 5. What TLS kept, lost, and added

- **Kept:** the NPC-arousal-plus-corruption stage gate (one instance — the shower walk-in); authored "carryover" handoffs (e.g. the high-corruption robe-open tease bumps Frank's arousal so it feeds the sex loop).
- **Lost / never had:** the player arousal fuel meter; the `>0` self-action switch; the on-screen arousal bar; the gallery freeze; the daily auto-rise.
- **Added (RTS has no equivalent):** automatic time-decay of NPC arousal.

---

## 6. Plain-language recap

- **RTS arousal = pressure that builds on its own and you release by climaxing.** You feel it constantly; building it *is* the gameplay loop. At max, the player meter is just cosmetic; the NPC meter at max is the green light for his hardest content.
- **TLS arousal = a warmth dial on the NPC that leaks if you neglect him and opens one door.** You barely notice it; most of the game ignores it.
- **Opposite directions:** RTS *accumulates*, TLS *evaporates*. If TLS ever wanted to feel like RTS, the missing piece is a **player arousal stat with a `>0`-style gate** on Maya-initiated content — which the engine currently has no primitive for. (Deferred.)

---

## 7. Anchors

**RTS** — see doc 38's anchor table (Story-JS function/line locators).

**TLS** (`games/the_long_summer_test/toml_phases/7_final_game.toml`):
- `[[traits.labels]]` `key = "arousal"` (NPC-subject trait declaration, ~L163).
- Per-NPC `core_traits = { love, trust, corruption, arousal = 0 }` (Frank/Jake/Ryan, ~L475/547/564). **No `player`/Maya arousal anywhere.**
- `[npcs.trait_decay]` `arousal = 1.0` (~L482).
- Representative effects: `{npc, trait="arousal", op="add", value=2/5}` teases (~L1987/2007/2930); `op="add", value=-3/-2` spend/frustration (~L3010/3069/4446).
- The lone arousal **gate**: Frank-shower substitution `arousal gte 30` (~L9202). The lone `set value=30`: dev capstone shortcut (~L8803).

**Engine** (`apps/game_generation/twee_comprehensive/generators/v2.py`):
- Arousal emotion bands: `_get_default_emotion_mappings` (~L9097).
- Per-day decay loop (`Math.max(0, trait − amount)`, skipped if `npc_interacted_today`): `advanceDay` (~L4332+).

---

*Companion: doc 38 (RTS Arousal System); memory `rts_arousal_system.md`. **The gap-closing engine PRD is doc 40 (Player Arousal Engine PRD).***
