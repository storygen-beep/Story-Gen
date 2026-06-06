# The four lanes — when to use each, and how to write them

NPC content uses four mechanisms (`doctrine/02`). They are the SAME canvas+trigger engine; the
"lane" is the *combination of trigger fields* (`schema/01` §3.3 fingerprints). An NPC arc is built
**across** lanes, sized by the NPC's arc shape (budget table below). Read this before authoring any
`npc_intro` / `arc_escalation` / `cross_npc` / `capstone` beat.

**Two companion references:** pick each NPC's gating *spine* — which trait drives the arc, by shape —
per `references/trait-design.md` (don't gate every NPC on `relation`). The repeatable explicit layer
(after the first-night capstone) is the **sex-loop menu**, its own pattern — `references/sex-loop.md`.

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

## Per-arc-shape budget — size to `doctrine/03` §2
Each shape has a per-lane canvas budget (L1 escalation rungs / L2 ambients / L3 walk-ins / capstones +
a total, FULL-game targets). **The authoritative matrix is `doctrine/03` §2 (Doc 56 §5) — size every
arc against it; it's the single source of truth, kept here as a pointer so the skill never drifts a
stale copy.** How the skill applies that budget:

- **Empty cells are honest** (§8.4). Peer/dating → no Lane 3. Service → no Lane 2 or 3. Filling an
  empty cell with texture is the failure, not the omission.
- **L1 cells count escalation *rungs*, not hubs.** Hubs are set by presence: **one Lane 1 hub per
  `[[npcs.schedules]]` row** (D72-R6). An NPC at 5 windows has 5 hubs even with a tiny rung budget —
  the extra hubs are *light* (base + talk + leave), exposure-capped.
- **Offscreen schedule rows are exempt from the hub rule.** A row at an `offscreen = true` location
  (the NPC's home/sleep/away block) is a non-navigable label — the player can't go there, so it gets
  NO hub and is exempt from the presence floor (`doctrine/10` §5.5, the Day System). Use offscreen
  rows to complete an NPC's day without manufacturing dead presence. Only **reachable** rows earn a
  hub; **locked** rows follow the unlock contract (§5.4).
- Author against the **shape**, never by cloning the gold-standard NPC (§8.5).
- **These are `full_game` targets.** At `scope_mode = slice` (see `setup-interview.md`), author
  ~30–50% of each budget for ONE gold-standard NPC + minimum-contract depth for the rest, with
  locked-visible rungs telegraphing the deferred remainder (`doctrine/03` §1). Read the game's
  `scope_mode` from the ledger before sizing an arc.

---

## Three surfaces at one location are SEPARATE canvases (`doctrine/02` §8.2/§8.3)
Where the player both interacts with an NPC AND does solo work at one location, that's THREE
independent canvases — the **NPC hub** (Lane 1), the **solo work canvas** (Maya-only,
location-triggered), and a **Lane 3 dispatcher** routing the NPC into the activity. Never put solo
work in the hub menu.

**Pronoun-in-the-verb test:** read each hub menu choice — if the NPC isn't the grammatical object, it
isn't Lane 1. "Pour **her** coffee" / "Tease **him**" → hub ✓; "Take a long shift" / "Wipe the booths"
→ solo work canvas, not the hub ✗.

---

## Lane 1 — hub button (how to write)
**Fingerprint:** `trigger_mode = "manual"`, `is_repeatable = true`, `location` + `npc` set,
`schedules` covering the NPC's window. Base node renders what the NPC is doing; `exit_block.choices`
IS the menu.
- **Choices = verbs with the NPC as object.** Vocabulary by register: **relational** (Talk — build
  trust), **self-display** (Tease, Flash), **contact** (grope, kiss), **explicit** (Have sex).
- **Label = the action, RTS-flat (not a literary sentence).** A choice label is a terse action verb,
  and the flavor lives in the scene the click opens, NOT in the label (`doctrine/05` one-beat-one-
  click). Strip self-justifying subtext: "Square the crate 😏", not "Square the crate. Ten minutes.
  Tell yourself it's just business." At explicit tiers put the crude word IN the label at the NPC's
  ceiling ("Suck his cock", not "Go down on him"). **Emoji: RTS-style on menu/hub buttons** (🔥 sex/
  seduce · 💬 talk · 🥃 pour · 💰 deal · ↩️ leave) — but **bare on in-loop cascade beats** (RTS's
  `<<linkreplace>>` beats carry none; see `references/sex-loop.md`).
- **Locked-visible ladder (§2.6):** ship the escalation rungs visible from day 1; a locked rung
  renders greyed with `show_when_locked = true` + its (versioned) `conditions`. Telegraphs the arc.
  **Two render modes — pick deliberately:** OMIT `locked_text`/`locked_text_threshold` → a **bare
  greyed span** showing the action text (the TLS look, the default); set `locked_text_threshold` → a
  clickable **button** that toasts the gate value (RTS `<<NotifyCorruption>>` style). Use the toast
  only if you actually want it — by default omit it.
- **Grey vs hide.** Only *escalation rungs* get `show_when_locked` (they telegraph the ladder).
  Daily-capped rungs, intra-loop beats, and conditional narrative branches **hide** (gated, no
  `show_when_locked`) — you don't telegraph "talk again tomorrow" or a pose inside the sex loop.
- **Hub cap ~5–6 items (§2.7).** More rungs → make them locked-visible stages, not parallel tasks.
- **Exposure-tier ceiling (§2.9):** the location's *privacy* caps which rungs may appear — Public
  (talk/look only) / Semi-private (tease/grope) / Private (full ladder). Relationship stats unlock
  rungs *within* that ceiling. Same-NPC hubs stay consistent (shared rung names/thresholds/voice).
- **Base + exit with zero unlocked choices is a complete, valid hub** (the presence floor). Never
  flag-gate the base node — gate the choices.
- **The hub opener is ONE constant paragraph (D56-R1, `doctrine/04` §1.1).** Do NOT tier the base
  node into T0/T1/T2 `[group]` blocks — the opening stays the same as the arc escalates; *only the
  choices* change. Tiering the opener is the Marge-Pass-1 failure. (Period-split hubs are different:
  a *separate* hub per schedule window is fine; tiering one hub's opener by stat is not.)

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
   study) MUST be **authentically not-about-the-NPC** — that's what makes the walk-in land. The
   energy/resource COST of doing it goes in **`costs`** (per-choice on the exit for a multi-intensity
   activity like work −15/−28, or trigger-level for a single-exit chore) — `costs` gates *and* deducts.
   NEVER put the energy spend in `exit_block.effects` (that decrements without gating → cosmetic
   meter) or gate it with `conditions`+`locked_text_threshold` (blue toast-button). `effects` carries
   only the *gains* (money/relation) + `time_progression_minutes`. See `toml-gotchas.md` "Resource gating".
2. **Dispatcher:** rolls dice + checks NPC conditions → HIT routes to the NPC scene, MISS plays solo
   content. **Each substitution target canvas ships ALL of:** `substitution_only = true` (keeps it
   out of the Lane 1/2 selectors) **+** `max_triggers_per_day = 1` (once-per-day is the felt cadence,
   D67-R7) **+** `is_repeatable = true` **+** a `location` (else it never enters the registry and the
   dispatcher silently misses — the C7b bug). All four are required; missing any is a known
   anti-pattern (`doctrine/02` §8.9/§8.10).
   - **Multiple mutually-exclusive variants at one activity (Pattern B):** give each rule the same
     `exclusive_group = "<name>"` string → ONE partitioned dice roll, fall-to-solo on a failed slot.
     Do NOT approximate with summed Pattern A `chance` values (wrong since Doc 69; `doctrine/02` §4.6.2).
   - **Walk-in direction:** Lane 3 walk-ins use a *loose* presence check (NPC is around — `IsNpcAtHome`
     style); a *strict* exact-location match is Lane 2 / Pattern C, not a walk-in (`doctrine/02` §4.8).
- **Vocabulary:** he walks in (mid-activity), he arrives while she's vulnerable, innocent setup →
  charged shift. The setup is genuinely a chore; the seduction happens *to* her.
- **A solo activity is also the game's earning/utility loop** — "work a shift" earns money and is the
  natural Lane 3 host. Splitting work (host) from the NPC hub (Lane 1) is the §8.2 rule in action.

## Lane 4 — capstone (how to write)
**Fingerprint:** `priority ≥ 9` (typically 9–12), `trigger_mode = "manual"`, auto-fire on location
entry when conditions match, flag-gated + sets a one-shot flag on completion. **Repeat field is one of
two forms** (`doctrine/02` §5.1):
- `is_repeatable = false` — once it fires, done; OR
- `is_repeatable = true` **+ a self-gate on its own setter flag** — the "retry" variant. The
  self-gate is a normal typed trigger condition on its OWN completion flag, e.g.
  `{ type = "flag", subject = "player", flag_key = "<its_setter_flag>", operator = "is_false" }`
  ("flag_is_false" is doctrine shorthand — emit the typed condition, NOT a literal `flag_is_false`
  key, which the engine ignores). The canvas re-fires next eligible time *until* its flag is set, so
  a **Refuse branch that doesn't set the flag keeps it alive** (Pattern F / F4). Canonical:
  `scene_franks_bedroom_evening` (in the `the_long_summer_test` game, not Late Shifts). Use this
  whenever a branching capstone has a decline path.

Three types (§5.2): **A** linear deterministic, **B** branching choice (Pattern F — both branches
playable, diverge in downstream effect), **C** quest-chain step. **Type-B forks follow Pattern F
sub-rules F1–F5** (`doctrine/04` §4): both branches good-faith, downstream divergence, fork at the
terminal beat, refuse-retry, no compounding. Per-NPC capstone budget per shape (table above). Voice:
Tier-3 earned (once-only, so the prose can spend).

**The repeatable layer comes after.** Capstones are the once-only *first* time; the replayable
explicit surface that follows (opened from the hub once the first-night flag is set) is the
**sex-loop menu** — its own pattern, see `references/sex-loop.md`.

## Voice register (`doctrine/03` §3.5)
- **Lane 1 / 2 / 3:** RTS-flat default — ~30-word caption density, direct/crude diction per the NPC's
  **per-tier vocab ceiling** (declared in its R7 brief; the ceiling model is `doctrine/08`, default-to-
  maximum-explicit). Re-readable (these repeat).
- **Lane 4 capstones:** Tier-3 EARNED — interior monologue + layered sensory detail +
  character-distinguishing diction. Once-only, so the prose can spend.
- **Choice labels** are tighter than the prose — label = action, no subtext, crude-in-label at the
  ceiling, emoji on menu buttons / bare on in-loop beats (Lane 1 above + `references/sex-loop.md`).

## Runtime rendering rules (live-verified — these bite even when the build is green)
The location screen renders four separate paths; a canvas only appears if it matches the right one:
- **NPC first-contact one-shot → make it AUTO-FIRE**, NOT an NPC-portrait canvas. `renderNpcPortraits`
  skips non-repeatable canvases, so a one-shot *with* `npc`/`requires_npc` set renders NOWHERE (it's
  neither a repeatable portrait nor an auto-fire). Author it like the boot canvas: `is_repeatable=false`,
  `priority≥9`, **no `npc`/`requires_npc`**, gated on flags; it auto-fires on entry and sets the
  `<npc>_opened_up` flag. The ongoing **hub** (repeatable, `npc` set) renders the portrait from then on.
- **Solo activity → no per-canvas `schedule`** if it should be available whenever the location is
  reachable. A `schedule` block on a solo activity suppressed its button (match the proven
  `activity_make_tea` shape: location + `is_repeatable` + `priority` + optional `conditions`/`substitutions`,
  no `schedule`). Gate availability via `conditions` and location reachability instead.
- **Distinct `name` per canvas.** A non-repeatable first-contact and its repeatable hub sharing a
  `name` collide in the name-group selector — give them different `name`s.
- **A hub portrait renders only while the NPC is present** (`getNpcLocation(slug).location == here`).
  If a hub won't show, verify the NPC's `[[npcs.schedules]]` actually places them at that location at
  the current time (and that schedule slugs resolved). Presence is the gate, not just `is_active`.

## Beat type → lanes (what a beat authors)
- `npc_intro` → establish the NPC's **Lane 1 hub(s)** (one per schedule row) + optionally the first **Lane 2** ambient. Cold-start enterable.
- `arc_escalation` → add **Lane 1 rungs** (locked-visible) AND the **Lane 2/3** content that lights up at those thresholds — per the shape's budget, respecting empty cells.
- `economic` → usually a **solo work activity** (Lane 3 host that earns money) + its dispatcher; keep it OUT of any NPC hub (§8.2).
- `cross_npc` → an NPC as interruptor in another's **Lane 3** ending, or a shared scene.
- `capstone` → a **Lane 4** one-shot gating a milestone.
- `location_reveal` / `story_turn` → structure + the scenes the new place/turn needs (often a hub + ambients).
