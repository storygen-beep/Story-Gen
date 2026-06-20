# Trait-gating audit — Last Call

*Recorded 2026-06-04. Facts-only: which traits actually gate NPC content in Last Call, which are
written-but-never-read, and how that compares to RTS. Descriptive — no pending tasks attached.*

Method: grep over `games/last_call/toml_phases/*.toml` for `trait_key`, `npc_X.relation`,
`*_stage`, and `arousal` in both conditions and effects.

---

## §1 — What actually gates NPC content

### Per-NPC stat used as a GATE: `relation` only
Every NPC capstone keys off `npc_X.relation` (14 condition uses total):

| NPC | relation gates |
|---|---|
| Sal | ≥ 45 (after-hours kiss), ≥ 60 (upstairs), ≥ 75 (backbone) |
| Dee | ≥ 20 (terms) |
| Marcus | ≥ 15 (singled out) |
| Rosa | ≥ 25 (trust talk) |

So **`relation` is the only per-NPC stat ever READ as a gate.** The user's observation is correct.

### Game-wide gating is NOT relation-only
The dominant gate across the whole game is **`player.corruption`** — 48 condition uses vs. 14 for
relation. It gates: Lane 2 hot variants (corr lt/gte N), Dee's deal (corr 25), Marcus's kept
arrangement (corr 50), clothing-wear unlocks, sex-loop pose unlocks. It's a **player-global** trait,
not per-NPC, so it doesn't read as "an NPC trait" — but it does most of the routing work.
Also: `money` (4 uses, reckoning fork) + sex-loop internals (`loop_npc_pleasure` 16,
`sex_finisher_type` 8, `anal_active` 6).

Net: **per-NPC gate = relation; global gate = corruption × money.**

---

## §2 — Traits written but NEVER read (the gaps)

### `npc.arousal` — dead meter (the real gap)
Incremented everywhere, read nowhere. **Zero `npc_X.arousal` conditions** exist.
- `+1/day` for Sal via `[engine.daily_tick].traitEffects` (cap 3).
- `+1` per interaction for Sal / Dee / Marcus (cap 3), in their first-meeting + Lane-2 + deal canvases.
- Player `arousal` (0–10) IS read indirectly (sidebar band + set to 0 at climax) but also never gates
  an NPC interaction.

This is the **RTS pattern half-built**: RTS uses NPC arousal (4 levels: ❄️/🔥/🔥🔥/🔥🔥🔥) as the
*Lane 2 tier gate* — "the higher the arousal, the further the events progress" (see
`lane2_reference.md` §2). Last Call copied the *climbing* half but tiers Lane 2 on **player
corruption** instead, leaving `npc.arousal` decorative.

### `*_stage` traits — set, never gated (intentional)
`sal_stage` / `marcus_stage` / `dee_stage` / `rosa_stage` are `op="set"` as each arc advances
(stage 1→4) but never appear in a condition. They feed the **arc-stage label / sidebar readout**
(matched against the NPC's `arc_stages` array), NOT logic. The real gate is the `relation`
threshold; the stage is the display. Hidden from the player via `[[traits.labels]] hidden=true`.
This is by design — they're labels, not gates.

---

## §3 — Summary

- **Per-NPC gating = `relation` only.** (Confirmed.)
- **Game-wide gating = `relation` (per-NPC) × `corruption` (global) + `money`.**
- **`npc.arousal` = wired-but-dead** — climbs, gates nothing. RTS uses it as a real second tier axis.
- **`*_stage` = labels, not gates** — intentional readout for the arc-stage display.

If a second per-NPC axis is ever wanted, the clean move is to make `npc.arousal` actually gate
something — e.g. tier the Lane 2 hot variants or sex-loop entry on `npc_X.arousal gte 2`
alongside/instead of player corruption — turning the dead meter into the RTS-style arousal axis.

### Sources
- `games/last_call/toml_phases/*.toml` (grep, 2026-06-04).
- `games/last_call/lane2_reference.md` (RTS Lane 2 tier system, §2).
