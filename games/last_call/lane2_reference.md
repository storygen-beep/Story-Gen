# Lane 2 reference — Last Call vs RTS

*Recorded 2026-06-04. A facts-only reference of how Lane 2 ("location-entry random" ambients /
"house events") is built in Last Call vs how Road to Success (RTS) does it. Descriptive only.*

---

## §1 — Last Call Lane 2 (as built)

Trigger = `requires_npc` + a `[[canvases.trigger.schedules]]` window + `trigger_mode = "random"` +
`chance`. **As of beat_0021 (2026-06-04) they are TIERED** via mutual-exclusion gates (the RTS
"same doorway deepens with stat" pattern, ported premise-appropriately): each peer ambient's base
is gated `corruption lt N` with a `_hot` variant gated `gte N`; the Collector's collection-night
ambient tiers on `bar_seized`. Voice stays RTS-flat (~30w, charged-but-bounded — not Tier-3).

| Canvas id | NPC | Window | Chance | Tier gate | Kind |
|---|---|---|---|---|---|
| `canvas_bar_ambient` | Sal | bar 17–02 | 0.25 | corr lt 25 | mood ("for a second it's just a bar") |
| `canvas_bar_ambient_hot` | Sal | bar 17–02 | 0.25 | corr ≥ 25 | brush-past behind the bar (hand on hip) |
| `canvas_marcus_ambient` | Marcus | bar 20–23 | 0.25 | corr lt 20 | being watched ("…later") |
| `canvas_marcus_ambient_hot` | Marcus | bar 20–23 | 0.25 | corr ≥ 20 | back-booth beckon; eyes follow all night |
| `canvas_dee_ambient` | Dee | depot 10–17 | 0.25 | corr lt 25 | made to wait ("wait your turn") |
| `canvas_dee_ambient_hot` | Dee | depot 10–17 | 0.25 | corr ≥ 25 | crooks a finger → the cellar |
| `canvas_collector_pressure` | Collector | bar Mon 18–20 | 0.3 | bar_seized false | prices the room (menace) |
| `canvas_collector_word` | Collector | bar Mon 18–20 | 0.3 | bar_seized false | deniable threat |
| `canvas_collector_coerce` | Collector | bar Mon 18–20 | 0.3 | bar_seized true | post-seizure coercion (it's his now) |

(Rosa has none — service NPC, empty Lane 2 by design.) The base/hot pairs are mutually exclusive,
so exactly one fires per tier — true escalation, not a flat single beat.

---

## §2 — RTS Lane 2 (complete, as found)

### The tier system (live-extracted from the in-game Game Mechanics page, mopoga v0.26)
House events are gated by two axes:
- **NPC arousal — 4 levels:** ❄️ not aroused · 🔥 slightly aroused · 🔥🔥 aroused · 🔥🔥🔥 highly aroused.
- **Player corruption stage** — starts "Pure", evolves to unlock new actions/scenes.

Verbatim from the game: *"This status directly affects indoor events—the higher the arousal, the
further the events progress. Corruption also plays a significant role."* and *"The available actions
and scenes depend on your corruption level… Your stage evolves—unlocking new actions and scenes."*

### The scenes + gates (catalog §2.1 + raw `passage_catalog.json`)
| Scene | Gate | Where / chance | Kind |
|---|---|---|---|
| `Stepbrother Bedroom Grope` | brother arousal 🔥 | your bedroom, 20% | passive grope on entry |
| `Peep Stepbrother Sex` | your corr 15 | his bedroom, 25% | walk in on him (voyeurism) |
| `Brother Caught Masturbating` | brother arousal 🔥🔥 + corr 10, your corr 30 | his bedroom, 25% | catch in the act → join/escalate |
| `BedroomGrope` | multi-NPC dice (`IsNpcAtHome("Dad")/("Brother")`) | your bedroom | whoever's home + aroused gropes you; 1 line + image + corruption tick |
| `DadPeepSex` / `DadPeepSexBedroom` | arousal/corruption inside | bathroom/bedroom | peep him having sex |
| `BedroomSleepDadScene` | random | your bedroom | proximity while sleeping |

### Tiered two ways
- **Across canvases:** multiple Lane 2 scenes share one location, each gated at a higher
  arousal/corruption threshold — so the same doorway rolls different content as you escalate
  (his bedroom: Peep at your corr 15, Caught at his arousal 🔥🔥 + corr 10 / your corr 30).
- **Within a canvas:** the scene's cascade deepens by stat. `DadPeepSex`: peek → *if aroused* →
  touch yourself → *if corr ≥ 2* → masturbate → climax. `BrotherCaughtMasturbating`: *corr ≥ 3* →
  full join cascade; else the *"Ew you pervert! Stop it!"* **rejection variant** with a published
  `NotifyCorruption(3)` threshold.

### Also gated on presence (confirmed live)
Entering the Stepbrother's room at Early Morning returned *"Your Stepbrother is not in his bedroom"*
(he was in the Kitchen) — the scene requires the NPC scheduled present, on top of arousal + corruption.

### Sources
- Live session on `https://mopoga.com/road-to-success` v0.26 (Game Mechanics passage text + House
  sidebar panel + the presence message), 2026-06-04.
- `prompts_v2/reference/02_rts_scene_catalog.md` (analyzed catalog, §2.1 Brother walkthrough table).
- `game_explorations/road_to_success/passage_catalog.json` (`source_raw` of the actual passages).

---

## §3 — A few points that are different (updated after beat_0021)
- **Tiering: now both tier** (was LC's gap). LC tiers via mutual-exclusion gates (base `corr lt N`
  ↔ `_hot` `gte N`; Collector pre/post `bar_seized`) — two tiers per surface. RTS tiers finer (4
  arousal levels × corruption stages) and ALSO *within* a scene (the cascade deepens beat-by-beat).
- LC premise = **workplace** (watched / made to wait → charged contact). RTS premise =
  **cohabitation** (groped / peeped on housemates). The *kinds* still differ by premise.
- LC kinds = mood / watching / waiting / menace (sharpening at the hot tier). RTS kinds = grope /
  peep / caught (charged sexual).
- LC beats ≈ 30 words even at the hot tier. RTS scenes can run long cascades (≈4,000–6,400 chars).
- LC has no **rejection variant** (it swaps base↔hot by stat). RTS bounces low-tier entries with a
  published "come back at corr N" threshold inside the scene.
- LC now has **two** ambients per surface (base + hot). RTS has **several** per location at finer
  thresholds.
- Same in both: Lane 2 requires the NPC **present** (schedule gate), and the same doorway yields
  deeper content as you corrupt.
