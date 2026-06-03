# The four lanes — when to use each, and how to write them

NPC content uses four mechanisms (`doctrine/02`). They are the SAME canvas+trigger engine; the
"lane" is the *combination of trigger fields* (`schema/01` §3.3 fingerprints). An NPC arc is built
**across** lanes, sized by the NPC's arc shape (budget table below). Read this before authoring any
`npc_intro` / `arc_escalation` / `cross_npc` / `capstone` beat.

## The lanes at a glance (`doctrine/02` §1)
| Lane | Who picks | Player POV | Intent |
|---|---|---|---|
| **1 — Hub button** | Player clicks a menu item | "I'll click Tease." | Intentional escalation; high agency |
| **2 — Location-entry random** | Dice on room entry | "I walked in and he was…" | Ambient coexistence; texture |
| **3 — Dispatcher substitution** | Dice inside a Maya-solo activity | "I was showering and he walked in." | Charged surprise; happens *to* her |
| **4 — Capstone** | Engine, on threshold cross | "The night he caught me." | One-shot milestone; point of no return |

## The master rule — Lane 1 leads (`doctrine/02` §6)
> Lane 1 leads the arc; Lanes 2/3 follow as consequences of Lane 1 escalation; Lane 4 capstones
> gate the milestones, fired by the stat/flag combos Lane 1 produces.

The player clicks Lane 1 → stats rise → at thresholds, Lane 2/3 content *lights up* and Lane 4
capstones fire. "The world fills out around me as I escalate." So: **every arc is enterable from a
cold start** (corruption 0, no flags) through ordinary presence — the Lane 1 hub's base renders
unconditionally (presence floor). Never gate an arc's entry on a stat only raisable *inside* that
arc (the "backwards on-ramp", §8.12).

## The 3×3 grid — mix lanes AND tiers (`doctrine/02` §7)
Within each lane, intensity scales with stat tier. A game that is all-one-lane feels wrong:
all Lane 1 = transactional "menu game"; all Lane 2 = inert/passive; all Lane 3 = no agency.
**Mix all three lanes across all three tiers → alive.** Lane 4 sits outside the grid (the milestones).

## Per-arc-shape budget (`doctrine/03` §2 / Doc 56 §5) — FULL-game targets
| Lane / Tier | Family/ambient | Slow-burn family | Peer/dating | Service | Antagonist |
|---|---|---|---|---|---|
| L1 escalation rungs | 3–6 | 1–3 | 1–3 | 1 (base) | 0–1 |
| L2 ambients | 4–7 | 0–2 | 1 (low) | 1 | 2–5 |
| L3 walk-ins | 4–7 | 1–3 (ARE the milestones) | **0** | **0** | **0 own** (interruptor in others') |
| Capstones | 4–6 | 3–5 | 3–4 | 1–2 | 1–2 |
| **Total** | **25–35** | **10–15** | **8–12** | **6–10** | **6–10** |

- **Empty cells are honest** (§8.4). Peer/dating → no Lane 3. Service → no Lane 2 or 3. Filling an
  empty cell with texture is the failure, not the omission.
- **L1 cells count escalation *rungs*, not hubs.** Hubs are set by presence: **one Lane 1 hub per
  `[[npcs.schedules]]` row** (D72-R6). An NPC at 5 windows has 5 hubs even with a tiny rung budget —
  the extra hubs are *light* (base + talk + leave), exposure-capped.
- Author against the **shape**, never by cloning the gold-standard NPC (§8.5).

---

## CRITICAL — three surfaces at one location are SEPARATE canvases (§8.2)
Do NOT put Maya-solo work/chores in an NPC's hub menu. At a location where the player both
*interacts with an NPC* and *does solo work*, author THREE independent canvases:
1. **NPC hub** (Lane 1) — Maya-with-NPC.
2. **Solo work canvas** (Maya-only, location-triggered) — the chore/shift/errand.
3. **Lane 3 dispatcher** — routes an NPC INTO the solo activity later.

**The pronoun-in-the-verb test (§8.3):** read each hub menu choice. If the NPC is NOT the
grammatical object, it does NOT belong in the hub.
- "Pour **her** coffee" / "Tease **him**" → NPC is the object → Lane 1 ✓
- "Take a long shift" / "Wipe the booths" / "Work the bar" → no NPC object → **solo work canvas, not Lane 1** ✗

---

## Lane 1 — hub button (how to write)
**Fingerprint:** `trigger_mode = "manual"`, `is_repeatable = true`, `location` + `npc` set,
`schedules` covering the NPC's window. Base node renders what the NPC is doing; `exit_block.choices`
IS the menu.
- **Choices = verbs with the NPC as object.** Vocabulary by register: **relational** (Talk — build
  trust), **self-display** (Tease, Flash), **contact** (grope, kiss), **explicit** (Have sex).
- **Locked-visible ladder (§2.6):** ship the full ladder visible from day 1; locked rungs greyed
  with `show_when_locked = true` + `locked_text` + `locked_text_threshold`. Telegraphs the arc.
- **Hub cap ~5–6 items (§2.7).** More rungs → make them locked-visible stages, not parallel tasks.
- **Exposure-tier ceiling (§2.9):** the location's *privacy* caps which rungs may appear — Public
  (talk/look only) / Semi-private (tease/grope) / Private (full ladder). Relationship stats unlock
  rungs *within* that ceiling. Same-NPC hubs stay consistent (shared rung names/thresholds/voice).
- **Base + exit with zero unlocked choices is a complete, valid hub** (the presence floor). Never
  flag-gate the base node — gate the choices.

## Lane 2 — location-entry random ambient (how to write)
**Fingerprint:** `trigger_mode = "random"`, `chance = 0.2–0.3`, `is_repeatable = true`,
`requires_npc`, `schedules`, optional stat `conditions`. Fires on entry, substitutes the hub render.
- **Vocabulary:** pass-by (NPC crosses with a mug), solo-activity glimpse (making coffee alone),
  passive contact (he gropes you as you pass), atmospheric voyeurism (you walk in on something).
- **NOT in Lane 2:** high-agency consummation (that's Lane 1 earned or Lane 4 scripted). Lane 2 is
  brief, charged-but-bounded contact.
- **In-fiction interruption (§3.6):** lower-tier endings must stop on a real beat — external
  (a kettle, a door), internal (she stops herself), or NPC-stopping (he lets go). Higher tiers blow through.
- Cooldown is engine-handled (3 visits) — don't author your own.

## Lane 3 — dispatcher substitution (how to write)
The hardest lane; RTS's biggest. Two canvases per activity:
1. **Solo-activity host (§4.4):** its own `[[canvases]]`, `trigger_mode = "manual"`,
   `is_repeatable = true`, `location`, `schedules`. The parent activity (work a shift, shower,
   study) MUST be **authentically not-about-the-NPC** — that's what makes the walk-in land. Menu
   gating (time/energy/money) lives on the location button; stat cost in `exit_block.effects`.
2. **Dispatcher:** rolls dice + checks NPC conditions → HIT routes to the NPC scene, MISS plays solo
   content. **Substitution canvases MUST declare a `location`** or they never enter the registry and
   the dispatcher silently misses (the C7b bug). Per-day cooldowns + per-arc Lane 3 budget apply.
- **Vocabulary:** he walks in (mid-activity), he arrives while she's vulnerable, innocent setup →
  charged shift. The setup is genuinely a chore; the seduction happens *to* her.
- **A solo activity is also the game's earning/utility loop** — "work a shift" earns money and is the
  natural Lane 3 host. Splitting work (host) from the NPC hub (Lane 1) is the §8.2 rule in action.

## Lane 4 — capstone (how to write)
**Fingerprint:** `is_repeatable = false`, `priority ≥ 9`, auto-fire on location entry when
conditions match, flag-gated + flag-setting. Three types (§5.2): **A** linear deterministic,
**B** branching choice (Pattern F — both branches playable, diverge in downstream effect),
**C** quest-chain step. Per-NPC capstone budget per shape (table above).

## Voice register (`doctrine/03` §3.5)
- **Lane 1 / 2 / 3:** RTS-flat default — ~30-word caption density, direct/crude diction per the
  game's vocab ceiling. Re-readable (these repeat).
- **Lane 4 capstones:** Tier-3 EARNED — interior monologue + layered sensory detail +
  character-distinguishing diction. Once-only, so the prose can spend.

## Beat type → lanes (what a beat authors)
- `npc_intro` → establish the NPC's **Lane 1 hub(s)** (one per schedule row) + optionally the first **Lane 2** ambient. Cold-start enterable.
- `arc_escalation` → add **Lane 1 rungs** (locked-visible) AND the **Lane 2/3** content that lights up at those thresholds — per the shape's budget, respecting empty cells.
- `economic` → usually a **solo work activity** (Lane 3 host that earns money) + its dispatcher; keep it OUT of any NPC hub (§8.2).
- `cross_npc` → an NPC as interruptor in another's **Lane 3** ending, or a shared scene.
- `capstone` → a **Lane 4** one-shot gating a milestone.
- `location_reveal` / `story_turn` → structure + the scenes the new place/turn needs (often a hub + ambients).
