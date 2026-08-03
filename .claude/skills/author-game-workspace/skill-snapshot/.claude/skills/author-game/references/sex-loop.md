# The repeatable-explicit sex-loop menu (how to build one)

Capstones (Lane 4) are the once-only *first* time. After that, an arc needs a **repeatable** explicit
surface or the hub goes hollow once the milestones are spent. The sex-loop is that surface: a
player-driven menu of acts/poses that climbs a pleasure meter to a chosen climax, replayable nightly.

Read this when a beat adds repeatable explicit content to an NPC whose per-tier vocab ceiling allows
it (the ceiling is declared in the NPC's design brief; model in `references/kink-ceilings.md`) — typically the gold
NPC's full arc, not service/antagonist. Reference implementation: `the_long_summer_test`
`loop_franks_bedroom_sex` (+ its finisher) — copy its table shapes.

## Shape at a glance
A **triggerless** canvas (no `[canvases.trigger]`) reached ONLY by node routing, plus a sibling
finisher canvas:

```
[hub rung] --nodeId--> intro --> base_<central pose>
                                   ├─ act result nodes  → loop back (raise pleasure)
                                   ├─ pose-switch choices → base_<other pose>  (set sex_stage)
                                   └─ climax-elect (gated on pleasure) → <finisher>.climax
<finisher>.climax → one choice per finisher type (group-blocked) → reset all loop traits → exit
```

## The two non-obvious rules (these are why it's a separate pattern)

**1. State is NUMERIC TRAITS, never flags.** A flag whose only setter is a triggerless (node-routed) canvas
DOES register as set — but with no location/schedule — so if any downstream canvas **trigger** or **choice**
requires it `is_true`, the build HARD-FAILS with `MISSING HINT - set by '<canvas>' but no location/schedule`
(`v2.py:11135`/`:11165`, raised as a `CommandError`, `package_from_toml.py:396`). (Not `NEVER SET` — the
canvas *is* credited as a setter; it just has no located hint.) Numeric traits aren't flag-chain-checked, so
loop state uses traits. Declare them in `[player.core_traits]` and hide them from the sidebar with
`[[traits.labels]] hidden = true`. **A milestone the loop must record** (e.g. "the drain happened") is the
same trap — express it as a hidden trait *counter* and gate the reader on the trait, not a flag. (`is_false`
guards, `[group]` conds, and quest `when` blocks are exempt — only trigger/choice `is_true` flag gates are
location-checked; trait conditions never are.) Canonical set:

| trait | meaning |
|---|---|
| `sex_stage` | which pose (0 foreplay · 1 oral · 2 … per your poses) |
| `loop_npc_pleasure` / `loop_player_pleasure` | the climbing meters |
| `sex_finisher_type` | which climax the player elected (0 facial · 1 inside · 2 ass · 3 body) |
| `anal_active` | 0/1 toggle set on a doggy/missionary rung |
| `sex_entry_origin` | which hub/location entered the loop (for origin-flavored prose) |

**2. Reset on entry, reset on exit.** The hub rung that routes in sets every loop trait to 0 (fresh
run); the finisher's exit choices set them all back to 0 (clean state for next time). Forget either
and the next run starts mid-climb.

## Building it
- **Routing:** `targetType = "node"`. Within the same canvas use a bare `nodeId = "base_doggy"`;
  cross-canvas use `nodeId = "<finisher_canvas>.climax"` (the `"<canvas_id>.<node_id>"` form).
- **Pose nodes:** each `base_<pose>` node's `exit_block.choices` are (a) 1–2 **act results** — a
  short beat that loops back (`nodeId` = same pose) and raises a meter, and (b) **pose switches** to
  other `base_<pose>` nodes (set `sex_stage`). Higher poses gate on player `corruption`
  (locked-visible if you want them telegraphed; see `lanes.md`). `anal_active = 1` toggles on a
  doggy/missionary rung gated at the corruption tier your ceiling sets.
- **Pleasure increment:** `effects = [{ targetType = "player", trait = "loop_npc_pleasure",
  op = "add", value = { type = "random", min = 8, max = 14 } }]`. (Random keeps the climb from feeling
  metronomic.) *Build note:* this emits a benign `'>' not supported between instances of 'dict' and
  'int'` warning from the trait-effect hint helper — it's a build-time hint only, runtime is fine
  (TLS emits it too). Don't "fix" it by removing the random.
- **Climax-elect:** a choice on each pose node, gated `loop_npc_pleasure gte <N>` (e.g. 50), that sets
  `sex_finisher_type` and routes to the finisher. Below the threshold the choice is simply absent.
- **Finisher canvas (triggerless):** a `climax` node whose choices are the finisher types — render the
  right prose with `[group]` blocks keyed on `sex_finisher_type` (one block per value). Each exit
  resets all loop traits to 0 and routes to a real location. Anal/inside variants gate on
  `anal_active`.

## Wiring it to the arc
The loop opens from the NPC's **Lane-1 hub** (or the after-close hub) as a rung gated on the
first-night flag the capstone set (`<npc>_first_done`). Make that rung **locked-visible**
(`show_when_locked = true`, no `locked_text_threshold` — see `lanes.md`) so the repeatable layer reads
as a coming destination rather than appearing from nowhere. The rung's `effects` do the entry reset.

## Variant: anonymous / paid service venue (no NPC arc)
The scoping line at the top (an NPC's full arc, "not service/antagonist") has ONE exception: a **paid/anonymous
venue** — a brothel, a bathhouse, a glory-hole hallway — runs the *exact same triggerless pose-ladder loop* for
a partner with no arc. Only the entry/exit wiring changes:
- **No NPC gate.** No `npc`/portrait, no `relation`/`corruption` gate on the loop. Gate the *venue* on access
  (a location/flag) + **coin** (can she afford it) + optionally **hygiene**; the partner is anonymous ("a john,"
  "a stranger"), so the loop traits carry no relationship state.
- **Pay ON FINISH, never the entry faucet.** Put the coin change in the **finisher's exit** effect, not the
  entry rung — an entry-charge (or entry-payout) is a faucet the player games by entering and bailing (a bug
  Vesper's brothel shipped and fixed). She earns/pays when the scene *completes*.
- **Upkeep drop on exit.** Hang the hygiene (and coin) change on the existing exit-reset (rule 2 — the finisher
  already zeroes the loop traits), so it's one clean place.
- **Cold register.** Extends the Voice section below — transactional, detached; graphic at the ceiling but no
  warmth, no relationship beats.
Everything else — the triggerless canvas, the trait-state rules (#1), pose gating, the `[group]` finisher — is
identical to the gold-arc loop above.

## Voice
In-loop labels are **bare + crude at the NPC's ceiling** (`Suck his cock`, `Bend over`, `Let him cum
inside you`) — no emoji on cascade beats (that's RTS's `<<linkreplace>>` register; see `lanes.md`
choice-vocab). The hub *entry* rung is a normal menu button (emoji per the hub style). Prose per act
stays RTS-flat (~30–50 words, re-readable) — this repeats, so don't spend Tier-3 here.

## Self-check before validating
- Loop + finisher canvases have **no** `[canvases.trigger]` (reached only via `nodeId`).
- All loop state is **traits**, declared in `core_traits` + hidden; **no flags** set inside the loop.
- Entry rung AND finisher exits both reset every loop trait to 0.
- Climax-elect appears only past the pleasure threshold; finisher prose group-blocks cover every
  `sex_finisher_type` value; anal variants gate on `anal_active`.
- Every `conditions` block carries `version = "1.0"` (`toml-gotchas.md`).
