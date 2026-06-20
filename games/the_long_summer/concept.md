# The Long Summer — Concept

*1-page pointer. Full design lives in `../19th_april_UOR_Redesign_Session/Game_Redesign.md`.*

## The premise

Maya, 18, arrives at her mother Diana's new house in a small rural Southern town — the house Diana shares with her new husband Frank and his two grown sons, Ryan and Jake. Maya's life collapsed a few weeks ago: her boyfriend cheated, she cheated symmetrically in revenge, her friend group shunned her, and staying with Diana is the only landing pad she has left.

The town doesn't live by the rules Maya was raised on. Flirt, grope, and transactional sex happen openly. Her shame — what she did at the end of her last relationship — is internal, not social. As she learns what her body and her wits can earn, the player decides which parts of her old moral code she keeps.

## Why this game exists

Three design commitments that distinguish it:

1. **Permissive register as craft.** Every sexual act is mechanical, not taboo-crossing. Dramatic weight sits on Maya's internal reaction, not social scandal.
2. **Corruption as a bundled axis, not a tier-track.** One `corruption` stat with 4 descriptive bands (Closed / Opening / Operating / Saturated) carries the whole transformation via `trait_words` sidebar text.
3. **Distributed self-recognition, not a scripted awakening.** The moment she realizes she's changed isn't a scene — it's the weather that moves through the prose of recurring scenes over weeks.

## The cast

- **Maya** — PC. 18, artist-inclined, hardened. Prologue-inherited calculation tier.
- **Frank** — stepfather. Disciplined landlord. Two-phase arc (Rules → catch-trigger → Sexual arc → Keep branches: romantic / arrangement / rupture / power-inverted).
- **Ryan** — stepbrother, peer-male labor. Used-equipment flip business with failing margins. Arc: Help → Partner → Big deal with sex → Beach + proposal → Keep branches.
- **Jake** — stepbrother, hostile artist. Draws nude women; secretly draws Maya once her beauty rises. Arc: hostile → noticed → peeking + drawing → caught → hand → Keep branches.
- **Diana** — mother. Widow remarried to Frank. Good relationship with Maya. Household rule-anchor, silent witness. **No Phase 1 arc.**
- **Marge** — diner owner. Simple employer. Hands Maya the Thursday-night key at Chapter 2's close.
- **Prologue cast (placeholders):** Daniel (ex), Emma (the other girl), Kevin (Emma's boyfriend, revenge target), Sarah (best friend).

## Structural choices

- **4 player phases** of play: Prologue (Phase 0, pre-rural collapse) → Phase 1 (the summer) → Phase 2+ (after Phase 1 close, Diana potentially activates, shadow layer potentially opens, truck stop bar + full college open).
- **3 NPC arcs run in parallel.** Each has its own trigger and clock. At most one Crack per chapter.
- **Diner tier system (0/1/2/3)** is the primary corruption-to-income translator.
- **Ryan's shop** is a secondary income channel gated on Maya's charm + corruption.
- **Economic pressure** — rent + college savings target — motivates escalation organically.
- **Phase 1 closing event is deferred.** Not designed until play exposes what the end should feel like.

## What's locked vs. what's TBD

- **Locked:** All 12 sections of `Game_Redesign.md` marked ✅ FINALIZED. Sub-reputation system. 4-tier diner. 10 player traits. All three NPC Crack beats. Frank's catch-trigger. Prologue's 4-act structure. Chapter 1 and 2 closing events.
- **Deferred:** Town name, exact economic numbers, Prologue cast names, Maya's midpoint crack, Phase 1 closing event, Ryan's specific big-ticket customer archetypes.

## Engine

The game runs on the TOML-based story-gen engine. F1–F4 changes (trait_words sidebar, entry_conditions clothing-gate removal, player trait_decay, rent eviction_mode) are all shipped per `../19th_april_UOR_Redesign_Session/Engine_PRD.md`. The 10 locked player traits are all `[player].core_traits` entries — no new schema primitives required.

## Status

See `session_state.yaml`. Design is locked; engine is ready; book-phase generation is the active work.
