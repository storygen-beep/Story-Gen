# Doc 57 — Capstone Doctrine (Lane 4)

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Doctrine — applies to all capstone canvases in current and future RTS-shaped sandbox games on this engine
**Supersedes:** nothing. Codifies what Doc 24 §10.8.C named as out-of-scope ("a fourth lane outside the repeatable-content discussion") + extends Doc 50 R1 (capstone-coverage rule) with content + voice rules for the canvas itself
**Sibling of:** Doc 24 (3 lanes mechanism), Doc 50 (Quest Card Shape — which references this doc's content via `ready_canvas`), Doc 56 (RTS Principles & Alignment — this doc adds Lane 4 to that framework)
**Triggered by:** strategic review session 2026-05-24/25. After consolidating the 3-lane doctrine in Doc 56, capstones remained uncovered — Doc 50 R1 had the quest-pointer rule, but content rules and per-NPC budgets and voice register weren't written. RTS source verification across 4 capstones (`SellingMyStepsister`, `VeronicaMeet`, `MarcusParkSex`, `SecretAdmirer`) + TLS source across 3 (`scene_franks_bedroom_evening`, `canvas_marge_interview`, `scene_ryan_first_date`) surfaced the three-type taxonomy + register split this doc locks.

---

## §1 — The question this doc answers

You have a scripted scene that should fire ONCE per arc — a first night, a hire, a confrontation, an arc-transitioning beat. It's not Lane 1 (player picks from a menu), not Lane 2 (dice on entry), not Lane 3 (dispatcher inside a chore). What rules govern this canvas?

The one-line rule:

> **A capstone is a one-shot story beat with `is_repeatable = false + trigger_mode = "manual" + priority ≥ 9` that auto-fires on location entry when conditions match. It earns Tier-3 prose because the player won't see it again.**

The five hard rules in §4 are the mechanical floor. The voice rule in §6 names why capstones get richer prose than Lane 2/3 ambients. §3 is the three-type taxonomy that determines what shape the capstone takes.

---

## §2 — What capstones are (and what they aren't)

Capstones live on the SAME canvas/cascade engine as Lane 1/2/3. The capstone-ness is in the *authoring*, not in a separate mechanism.

### Mechanical fingerprint

| Field | Value | What it does |
|---|---|---|
| `is_repeatable` | `false` | Once it fires, it can't re-fire |
| `trigger_mode` | `"manual"` | Doesn't appear in Lane 1 portrait grids or Lane 2 random pools |
| `priority` | typically 9–12 | High enough to win against Lane 2 randoms on entry |
| `conditions` | narrative flag gates + trait gates | The story logic that says "now is when this fires" |
| `schedules` | optional time window | Constrains to specific times when fictionally appropriate |
| Flag effect on completion | sets a one-shot flag | This flag gates downstream content (Doc 50 R4 chain continuity) |

Engine entry point: `selectAutoFireCanvasForLocation` at `v1.py:3236`. When the player enters a location, the engine walks all canvases tagged to that location; if a capstone's conditions match AND it hasn't fired (`is_repeatable = false` + its setter flag is_false), it REPLACES the hub render entirely. ONCE.

### What separates a capstone from Lane 1/2/3

| | Lane 1 | Lane 2 | Lane 3 | Lane 4 (capstone) |
|---|---|---|---|---|
| `is_repeatable` | `true` | `true` | `true` | **`false`** |
| `trigger_mode` | `"manual"` | `"random"` | `"manual"` | **`"manual"`** |
| Who fires it | player picks from portrait/menu | dice on location entry | dice inside a chore | **auto-fires on location entry** |
| How often per arc | many | many | many | **once** |
| Cascade content register | RTS-flat | RTS-flat + specific detail | RTS-flat + specific detail | **Tier-3 literary** |
| Player choice fork | end of cascade | rarely | rarely | **sometimes (Type B)** |

### What capstones are NOT

- **NOT a separate engine path requiring new primitives.** The engine already handles them via `selectAutoFireCanvasForLocation`. No new code needed.
- **NOT every once-only scene.** A one-shot Lane 1 menu rung is still Lane 1 even if `is_repeatable = false`. The capstone definition requires auto-fire on entry, not player click.
- **NOT bigger automatically.** Length varies (1,200–10,600 chars across the sample). A short focused capstone (canvas_marge_interview, 1,900 chars) is just as valid as a long cascade.
- **NOT always Pattern F branching.** Only Type B has real choice forks. Type A and Type C are linear authored cascades.

### One-shot Lane 3 capstones (hybrid category)

A canvas can be mechanically Lane 3 (`substitution_only = true`, fires via the activity dispatcher path) yet narratively a capstone (gated by a `flag_is_false` self-gate, sets a one-shot story flag, has a quest card pointer). This is a hybrid: Lane 3 by mechanism, capstone by narrative function.

Worked example: `scene_frank_sleepover` (verified line 7531) has `priority = 4` + `is_repeatable = true` + `substitution_only = true` — fails the Lane 4 R1 trigger fingerprint (priority < 9, fires via dispatcher not auto-fire). But it's gated on `frank_sleepover_done is_false` + sets `frank_sleepover_done` on its exit, and it's referenced by Frank's F4 quest card. Narratively it's the fourth capstone in Frank's chain.

How to classify and what rules apply:

- **R1 trigger fingerprint does NOT apply** (the canvas fires via Lane 3 dispatcher, not via `selectAutoFireCanvasForLocation`).
- **R3 (quest-card pointer) DOES apply** — Doc 50 R1 requires the pointer regardless of which engine path delivers the scene.
- **R4 (Type C chain continuity) DOES apply** — the canvas is part of a chain by virtue of its setter flag gating downstream content.
- **F1–F5 apply if the canvas has a Pattern F fork**, identical to Lane 4 Type B.
- **Voice register (§6): Tier-3** — same as Lane 4 capstones, because the canvas is once-only.

Pick this shape when the fiction calls for the NPC to "happen" to be present (matches Lane 3's charged-surprise framing — "you ended up in his bed by morning, you didn't auto-walk in") rather than auto-fire on entry. The Lane 3 dispatcher requires a parent activity to substitute against — for sleepover, the player's solo activity at the bedroom location is the parent surface.

Verified across 4 RTS capstones + 3 TLS capstones. Every capstone is exactly one of these.

| Type | What it is | Structural shape | RTS example | TLS example |
|---|---|---|---|---|
| **A** Linear deterministic | Single authored cascade through N beats, no branching. Sets a story flag. | One node, N beats via cascade, no Pattern F fork | `VeronicaMeet` (10,602ch), `MarcusParkSex`, `MarcusBedroomSex1` | `canvas_marge_interview` (1,900ch), `scene_ryan_first_date` |
| **B** Branching choice | Cascade with a real Pattern F fork at a decision beat. Each branch is a different downstream node OR a different downstream arc entirely. | Cascade → fork → two distinct downstream nodes | `SellingMyStepsister` (7,837ch — Accept → Josh's sex cascade + arc transfer; Refuse → 2 lines + return) | `scene_franks_bedroom_evening` (Beat 2 → "Cross to him" climax node / "Hesitate. Step back" refuse node) |
| **C** Quest-chain step | Step-N in a multi-step authored chain. Each step's flag gates the next. Often time-delayed or DM-driven. | Multiple capstones in sequence, each Type A or B individually | RTS Edward DM arc (Pornstar DM → Date → Threesome — 3 chained capstones) | Frank declaration chain (catch → first-night → declaration → sleepover → Diana confrontation — 5 chained capstones) |

### Type A — Linear deterministic deep scene

**Use for:** first meets, intros, scripted character moments, hire/employment events, single-beat capstones where the player needs to BE in this moment but doesn't need to make a choice.

**Body shape:** one `[[canvases.nodes]]` with N cascade beats. Each beat has `advance_text` (the click that unfolds it). Final beat ends in the exit_block — usually a single "Return" or "Continue" choice that sets the flag and exits.

**Sample structure (canvas_marge_interview, verified):**

```toml
[[canvases.nodes]]
id = "interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg", ... } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off..." },
  { type = "dialog", npcId = "npc_marge", content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once..." },
  { type = "dialog", npcId = "npc_marge", content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across..." },
]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
[effects + flagEffects]  # sets hired_at_diner = true
```

No fork. The "Take the apron" exit is the only path forward; the player has already implicitly accepted by the time the cascade ends. The flag fires; the scene retires.

### Type B — Branching choice capstone

**Use for:** points of no return where the player's call must matter — cross-NPC arc transfers, partner commitments, irreversible declarations.

**Body shape:** cascade reaches a fork beat. The beat's `advance_text` is REPLACED by two distinct exit choices in `exit_block.choices`, each pointing at a different downstream node. The downstream nodes are full sub-cascades; usually the "accept" path continues the scene and "refuse" or "alternative" path is shorter + sets a different flag (or fails to set the primary flag).

**Sample structure (scene_franks_bedroom_evening Beat 2 fork, verified):**

```toml
# Cascade: Beat 0 (hallway), Beat 1 (push door), Beat 2 (close door — TERMINAL of cascade)
# Beat 2 ends with "Come here." — then exit_block.choices forks:

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
# Effects: player.corruption +1 (the crossing IS the corruption tick)

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# No effects. Refuse path does NOT set frank_bedroom_first_done — canvas can re-fire next eligible night.

# Then two more [[canvases.nodes]] declarations: node_first_night_climax + node_first_night_refuse
# Each with its own cascade + exit_block.choices for the post-fork content.
```

**Critical design property of Type B:** the refuse path is NOT a clean alternative outcome. It's a SHORTER scene. RTS's `SellingMyStepsister` Refuse path is two lines + return; the Accept path is 15 nested linkreplaces. TLS's `scene_franks_bedroom_evening` Refuse path doesn't even set the chain-completion flag — the player can come back another night and re-attempt.

Type B is *expensive to author* (two downstream paths, both must read as real options, the refuse must not feel like a punishment-button-don't-press-this). One per NPC arc is plenty.

### Type C — Quest-chain step

**Use for:** multi-beat narrative arcs where the player progresses through distinct authored moments — relationship escalation, career-arc unlocks, slow-burn revelations.

Each individual capstone in a Type C chain is either Type A or Type B internally. The "Type C-ness" is the CHAIN shape — Capstone1 sets Flag1, which gates Capstone2, which sets Flag2, which gates Capstone3, etc. Doc 50 R4 (chain continuity) governs the gating.

**Frank's chain (verified):**

```
scene_livingroom_catch  (Type A — sets frank_caught)
→ scene_franks_bedroom_evening  (Type B — sets frank_bedroom_first_done on Accept path)
→ scene_frank_declaration  (Type A — sets frank_cracked)
→ scene_frank_sleepover  (Type A — sets frank_sleepover_done)
→ scene_diana_confrontation  (Type A — sets diana_confronted)
```

Each capstone is one beat in the chain. The flag-setter pattern means the chain is BOTH the trigger condition for the next AND the quest-card pointer (per Doc 50 R1 + R4).

---

## §4 — Hard rules (R1–R5)

### R1 — Capstone trigger fingerprint

A capstone MUST have all of these:

- **EITHER** `is_repeatable = false` **OR** `is_repeatable = true` AND `conditions` contain a `flag_is_false` gate on the setter flag itself. Both patterns produce one-shot behavior; the `true + self-gate` variant supports Refuse-path retry (see F4). Worked example: `scene_franks_bedroom_evening` uses `is_repeatable = true` (verified line 3327) + condition `frank_bedroom_first_done is_false` (line 3336) — the Refuse branch doesn't set the flag, so the canvas re-fires next eligible night. `scene_frank_declaration` (line 7422) + `scene_frank_sleepover` (line 7538) follow the same pattern.
- `trigger_mode = "manual"` (default, no need to declare explicitly if engine treats it as default)
- `priority ≥ 9` (high enough to win against Lane 2 randoms on entry; 9 is the minimum, 10–12 for chain-final beats)
- `conditions` block including the flag-is_false gate that prevents re-fire (e.g., `frank_caught is_false` on the catch capstone). With the `is_repeatable = true + self-gate` variant, the same `flag_is_false` gate serves both R1 (prevent re-fire) and F4 (allow Refuse-path retry).
- A flag effect on at least one exit choice that sets the corresponding setter flag (so the canvas retires after firing on the Accept path)

A canvas missing any of these is NOT a capstone — it's either Lane 1 (if `is_repeatable = true` + portrait-clickable + no self-gate) or something miscategorized. Validation should flag any `is_repeatable = false + priority ≥ 9 canvas` that doesn't have a setter-flag effect, and any `is_repeatable = true + priority ≥ 9 canvas` whose conditions don't include a self-gate flag.

### R2 — Type-A simplicity preference

Default to Type A. Use Type B only when the player's decision MATTERS in a downstream-divergent way.

Concrete rule: if both branches of a proposed Type B fork would set the same flag and lead to similar downstream content, it's not a real fork — collapse to Type A. Type B is reserved for moments where:
- The two paths set DIFFERENT flags (the refuse path doesn't set the chain-completion flag), OR
- The two paths route into different NPC arcs (cross-NPC transfer like RTS `SellingMyStepsister` Brother → Josh), OR
- The two paths have materially different downstream content (one continues the cascade, the other ends short)

*Why this rule exists:* Type B is the most expensive capstone to author and the most cognitively expensive for the player (they must believe the choice matters). TLS currently has Type B at ~50%+ of capstones — high relative to RTS's ~25%. Not a violation, but a forcing function: each Type B should justify its cost.

### R3 — Capstone references in quest cards (Doc 50 R1 restated)

Every capstone (priority ≥ 9, is_repeatable = false, flag-setting) MUST be referenced by some quest_card's `ready_canvas` field — OR be explicitly marked off-panel with the `# off-panel:` comment.

This is Doc 50 R1 verbatim. Restated here for capstone authors who land in Doc 57 first.

### R4 — Type C chain continuity (Doc 50 R4 restated)

Every "post-X" capstone in a Type C chain (one whose `conditions` requires `flag_X = is_true`) MUST have a sibling "pre-X" capstone whose exit-flag-effect sets X.

This is Doc 50 R4 verbatim. Restated for chain capstones.

### R5 — Capstone schedule and location coherence

If a capstone has a `schedule` (time window), the schedule must match the fiction of the scene. *"Frank declares himself in the living room"* should fire in the living room schedule for evenings, not at 3 AM in the kitchen. If a capstone's location/schedule choice was made for engine convenience rather than fictional coherence, the fiction is bent and the player will notice.

The schedule + location combination ALSO determines who's likely in the room when the capstone fires. If Diana's awareness is meant to be the cost of the scene, the capstone should fire at a time when she's nearby — and the conditions can include her presence/absence flag explicitly.

---

## §5 — Per-NPC capstone budgets by arc shape

Refining the §5 distribution table from Doc 56 with the type breakdown.

| Arc shape | Type A | Type B | Type C chain length | Total capstones |
|---|---|---|---|---|
| **Family/ambient** (Frank) | 1–2 (first night, terminal scene) | 1–2 (first-night fork, declaration fork) | 4–5 (catch → first-night → declaration → sleepover → final) | 3–6 |
| **Slow-burn family** (Jake) | 1–2 (transition reveal, charged consummation) | 0–1 (revelation fork) | 2–3 (transition → revelation → relationship turn) | 2–5 |
| **Peer/dating** (Ryan) | 1–2 (first date, commit) | 0–1 (commit-or-break fork) | 2–3 (first date → second date → partner-or-break) | 2–5 |
| **Service** (Marge) | 1 (hire) | 0 | 1–2 (hire → mid-arc escalation if vocabulary allows) | 1–3 |
| **Antagonist/witness** (Diana) | 1–2 (confrontation, resolution) | 0–1 (resolution fork) | 1–2 (confrontation → resolution) | 1–3 |

**Ratio guidance:** Type B should be roughly 20–25% of an arc's capstone count, matching RTS's observed pattern. Higher Type B ratio (TLS Frank currently ~40%) means the arc is choice-heavy; lower means it's authored-fated. Either can be intentional; just know which.

**Total capstones per NPC arc:** small (1–3 for service/antagonist), medium (2–5 for peer/slow-burn), large (3–6 for family/ambient). An arc with 7+ capstones is doctrine drift — collapse some into Lane 1 menu items or Lane 2 ambients.

---

## §6 — Voice register

Capstones get Tier-3 prose. Lane 1/2/3 don't.

### What Tier-3 means in TLS

Tier-3 = the rich register reserved for once-only scenes:

- Interior monologue and observation tied to memory (*"the boards she knows the squeak of from the wrong side"*)
- Layered sensory detail per beat (multiple physical observations woven into one paragraph)
- Character-distinguishing diction (Frank's "girl" / "quiet", Marge's "hon", Ryan's "okay, good")
- Composed rhythm — sentences of varying length, deliberate cadence

### What Tier-3 is NOT

- Not generic literary prose. Specific to the scene's people and place. Frank's first-night opener invokes the specific hallway boards, the runner Diana picked out, the specific bathroom door. Not "the dim hallway in the quiet farmhouse."
- Not melodramatic. The prose stays controlled. Frank's "Quiet." carries the weight; the prose around it doesn't underline it.
- Not unlimited length. Frank's first-night cascade is ~5,000 chars across multi-node; canvas_marge_interview is ~1,900 chars. The prose density is HIGH; the scene length is bounded by what the moment needs.

### Why capstones earn Tier-3 (and Lane 2/3 don't)

A Lane 2 ambient fires 10–20 times across an arc. Authoring it with Tier-3 prose costs the same EACH TIME the player sees it, and after the third reading the language starts to feel performative. Lane 2/3 prose is built to be *re-readable without grating* — that's why it stays RTS-flat structure with specific detail.

A Type-A or Type-B capstone fires ONCE. The player won't see it again. The prose can be denser because there's no re-reading.

Type C chains use Tier-3 across all their capstones because each beat is once-only. Even when there are 5 chained capstones (Frank), each individual one only fires once.

### Anti-pattern: Tier-3 voice leaking into Lane 2/3

If a Lane 2/3 canvas contains interior monologue, extended metaphor, or memory-callback prose ("she remembered the way the kitchen had looked..."), the prose has drifted. The fix: extract that prose and move it to a capstone, then write the Lane 2/3 canvas with RTS-flat + specific detail.

### Anti-pattern: RTS-flat-bland voice in capstones

The inverse drift: a capstone written with generic Lane 2 prose. This wastes the once-only nature of the scene. If the player isn't going to read this again, the prose should EARN that single read by being specific, layered, and resonant. RTS-flat-bland in a capstone reads as a missed beat.

---

## §7 — Pattern F (Type B) guidelines

When a capstone IS Type B, the fork must be authored to specific standards.

### F1. Both branches must be playable in good faith

Neither branch can read as "the wrong choice." The Accept and Refuse must both feel like real options Maya could plausibly pick. If one branch is *clearly* what the player should do, it's not a real fork — it's a tutorial gate dressed up.

RTS `SellingMyStepsister` does this well: Accept = $500 + cross-NPC arc opens; Refuse = two lines + return. The Refuse is short but doesn't punish — it's an honest "no." Both are playable; the player chooses.

TLS `scene_franks_bedroom_evening` does this well: "Cross to him" = the climax cascade; "Hesitate. Step back" = a refuse-and-leave path that doesn't set the chain-completion flag (so the capstone can re-fire next eligible night). Refuse-now-accept-later is a legitimate playthrough.

### F2. The branches must diverge in DOWNSTREAM effect, not just text

If both branches converge to the same flag and the same next state, it's not a Type B — collapse to Type A with two flavors of the same outcome.

Real divergence:
- Different flag set (refuse doesn't set the chain-completion flag)
- Different NPC arc opens (cross-NPC transfer)
- Different downstream cascade content (continues vs. cuts short)
- Material trait effect difference (corruption +5 vs. +0; love +3 vs. love -2)

If none of these differ, you don't have a real fork.

**Borderline Type B (shared primary flag with secondary-effect divergence).** Some Type B capstones set the *same primary progression flag* on both branches but diverge in secondary effects — different reputation deltas, different trust modifiers, different sibling flags. Acceptable when the secondary divergence is *real downstream content*, not cosmetic text.

Worked example: `canvas_first_sunday_morning` (verified line 1660). Both choices ("Pay the sixty. Walk to the service with Diana." / "Pay the sixty. Stay home with the sketchbook.") set the same primary flags — `first_sunday_passed` + `first_rent_paid` — because the rent-and-week-passed *progression* must complete either way. The divergence is in secondary state:

- **Church path** additionally sets `attended_church_this_week` + `talked_to_diana_morning`, grants `rep_church +3`, Diana trust +2, Frank trust +2, Diana awareness −2, time +180.
- **Home path** sets nothing extra, grants Frank trust +1, time +60.

Both `rep_church` and the `awareness −2` Diana effect feed real downstream content (church regulars unlock dialog tracks; Diana awareness affects when `scene_diana_confrontation` fires). The branches genuinely diverge in long-tail consequence, even though the immediate quest-progression flag is identical.

Collapse to Type A (with branch-effects) only when secondary effects are also identical — that's two flavors of one outcome, not a real fork. Borderline Type B is valid; nothing-secondary Type B is not.

### F3. The fork beat should be the cascade's TERMINAL beat

The cascade plays through to the moment of decision. The decision is the LAST authored act before exit_block.choices fork. Don't have the player make the choice mid-cascade with N beats of authored content downstream of both branches — that's just two parallel scenes glued together. The fork is the moment of decision; everything after is downstream of that decision.

### F4. Refuse paths can keep the canvas alive for retry

If the refuse path doesn't set the chain-completion flag, the capstone can re-fire next eligible time. This is legitimate. `scene_franks_bedroom_evening` Refuse is exactly this — Maya can hesitate tonight and accept tomorrow.

If the refuse path DOES set the flag (or a sibling flag that closes the arc), the capstone is irreversible. Either side is valid; the choice should match the fiction. *"Sell my stepsister"* is irreversible — Refuse should close that scene's possibility. *"Cross to him in the bedroom"* is reversible — Refuse should let Maya try again.

### F5. Don't compound Pattern F with mid-branch tier-routing

`scene_franks_bedroom_evening` currently does this — the climax node has T0 (corruption < 40) vs T1 (corruption ≥ 40) closing register inside the Accept branch. Two structural devices stacked. This is the upper bound of complexity per capstone; don't push further (e.g., a three-way fork with tier-routing in two of the branches). The player loses the structural read.

---

## §8 — Worked examples

### Example 1 — `canvas_marge_interview` (TLS, Type A)

```toml
id          = "canvas_marge_interview"
description = "First visit to the diner. Marge sizes Maya up in 90 seconds, hires her on the spot. Fires once, gated on hired_at_diner == false."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false
priority      = 9
conditions = [{ flag_key = "hired_at_diner", operator = "is_false" }]

[[canvases.nodes]]
id   = "interview"
blocks = [
  { type = "image", ... },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", npcId = "npc_marge", content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", npcId = "npc_marge", content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it. Cookie's in the back, she'll show you the float." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
flagEffects = [{ flag = "hired_at_diner", op = "set" }, ...]
```

**Why this is exemplary Type A:**
- Single beat sequence, no fork. Marge has decided; Maya is recipient. No "Refuse the job" branch — the fiction is that Marge wasn't waiting for an answer.
- Length: 1,900 chars — *focused, not long.* Type A doesn't have to be 10,000 chars to count.
- Voice: Tier-3 in specifics ("up-and-down a woman who had hired forty waitresses did. The shoes. The hands."). The character is established in 6 sentences.
- Trigger fingerprint clean: `is_repeatable = false` + `priority = 9` + flag-gate + flag-effect on exit. R1 ✓
- Quest-card pointer required per R3 — Marge M1 capstone card has `ready_canvas = "canvas_marge_interview"`. ✓

### Example 2 — `scene_franks_bedroom_evening` (TLS, Type B)

```toml
id          = "scene_franks_bedroom_evening"
description = "Stage 4 FIRST-NIGHT cascade. Pattern E linear cascade + Pattern F fork at Beat 2."

[canvases.trigger]
location      = "loc_franks_bedroom"
requires_npc  = "npc_frank"
is_repeatable = true       # see note below
priority      = 9
conditions = [
  { flag_key = "frank_caught",                operator = "is_true"  },
  { flag_key = "frank_bedroom_first_done",    operator = "is_false" },
  { trait_key = "corruption",                  operator = "gte", value = 25 },
]

[[canvases.nodes]]
id   = "base"
blocks = [
  { type = "cascade", props = { beats = [
    # Beat 0: hallway approach (Tier-3 prose)
    # Beat 1: push the door open
    # Beat 2: close the door — TERMINAL of cascade, fork follows
  ]}}
]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [{ trait = "corruption", op = "add", value = 1 }]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# No effects. Does NOT set frank_bedroom_first_done — canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets first_done + tier-routed closing)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits)
```

**Why this is exemplary Type B:**
- F1 ✓ — Both branches playable. "Cross to him" = consummation. "Hesitate. Step back" = honest refusal, Maya can come back.
- F2 ✓ — Branches diverge in flag-effect (climax sets first_done; refuse doesn't) and in downstream content (climax = full sex cascade; refuse = brief disengage).
- F3 ✓ — Fork is at the terminal beat of the opening cascade ("Close the door."). Decision is the last act.
- F4 ✓ — Refuse keeps the capstone live. Maya can try again.
- F5 ⚠️ — Compounds Pattern F with mid-branch tier-routing inside the climax node (corruption < 40 vs ≥ 40 closing register). Just within the upper bound; don't push further.

**Note on `is_repeatable = true` here:** the canvas is marked `is_repeatable = true` but the conditions include `frank_bedroom_first_done is_false`, which means the FLAG gates re-fire rather than the `is_repeatable` field. Functionally identical to `is_repeatable = false`. Both patterns are valid; the conditions-flag pattern is preferred when the canvas might need to re-fire conditionally (e.g., refuse path leaves it alive).

### Example 3 — RTS `SellingMyStepsister` (Type B, cross-NPC)

```twine
:: SellingMyStepsister
[Cascade: Brother proposes the deal, names $500, Maya asks for clarity]

<<linkreplace "What?!">> ... <</linkreplace>>
<<linkreplace "$500? That's a lot of money!">> ... <</linkreplace>>

<div id="acceptSelling">
<<if getCorruptionLevel() >= 3>>
  <<linkreplace "Accept">>
    [Josh arrives, sex cascade across 15 linkreplaces, $500 grant, UnlockNPCScene Josh ...]
  <</linkreplace>>
<<else>>
  <<NotifyCorruption 3>>  /* gate published, no escalation */
<</if>>
</div>

<div id="refuseSelling">
<<linkreplace "Refuse">>
  Maya: "Get out of here, I'm not a prostitute!"
  Brother: "Sorry, I didn't know you would get offended"
  [Sets Josh.scenes.SellingMyStepsister.executedToday = true]
</<<linkreplace>>
</div>
```

**Why this is exemplary Type B (RTS canonical):**
- F1 ✓ — Both branches playable. Accept = explicit cross-NPC transfer. Refuse = clean no.
- F2 ✓ — Cross-NPC arc transfer is the strongest possible divergence: Accept opens Josh's arc entirely; Refuse keeps Brother's chain on its current track.
- F3 ✓ — Fork at the cascade's terminal (after Brother names the $500 and asks for the answer).
- F4 — Refuse sets `Josh.scenes.SellingMyStepsister.executedToday = true` (not the lifetime flag) — leaves the door open for the canvas to re-fire on subsequent days. Different policy from `scene_franks_bedroom_evening`'s Refuse but legitimately so.
- F5 ✓ — Doesn't compound with tier-routing inside the Accept branch. Single structural device.

---

## §9 — Anti-patterns

- **`is_repeatable = true` capstone.** A canvas with high priority + flag-setting effect but `is_repeatable = true` and no flag-gate to prevent re-fire. Will fire repeatedly. Caught by R1.
- **Capstone with no flag-setter on exit.** Fires once, then never again because no flag changed — but the canvas itself stays triggerable. Engine will re-fire it. Caught by R1.
- **Type B with collapsible branches.** Two branches that lead to the same flag, same downstream, with cosmetic text differences. Not a real fork. Caught by F2.
- **Type B fork mid-cascade.** The decision is at Beat 3, but Beats 4–8 are authored downstream of BOTH branches in parallel — two scenes glued together. Caught by F3.
- **Type B refuse-as-punishment.** The Accept branch is rich; the Refuse branch is a snarky one-liner that signals "don't pick this." Not a real fork. Caught by F1.
- **Tier-3 voice in Lane 2/3 prose** (cross-doc with Doc 56 R2). The capstone register leaked into a repeatable scene. Re-reading the canvas grates.
- **RTS-flat-bland voice in capstone.** Once-only scene written like an ambient. Wastes the canvas. Caught by §6 register doctrine.
- **Capstone with no quest-card pointer.** Doc 50 R1 — every priority ≥ 9 + is_repeatable = false + flag-setting canvas must be referenced by some quest_card OR have an off-panel comment. Restated as R3.
- **Type C chain with a floating step.** Capstone3 requires Flag_2, but no capstone sets Flag_2 — chain broken. Caught by R4 (Doc 50 R4).
- **Pattern F compounded with tier-routing AND multi-step downstream cascades.** Three structural devices stacked. Player can't read the structure. Caught by F5.

### NOT an anti-pattern: identical-prose duplicate-trigger capstones

When an engine constraint forces multiple canvases for a single narrative moment, authoring identical body prose across the duplicates is acceptable — the canvases represent two mechanical routes to the same narrative beat, not two distinct beats. Mark the duplicates with a comment naming the constraint that forced the split.

Worked example: `transition_jake_to_1_via_beauty` (verified line 2828) and `transition_jake_to_1_via_glance` (line 2866) share verbatim body prose. The file comment at line 2806 explains: *"Pre-refactor a single transition_jake_to_1 canvas watched a jake_stage_1 helper with OR-logic. OR in stage_helpers is now banned (validate() rejects it) because the resulting Pattern 2 goal block rendered as awkward 'Path A / Path B'. RTS-aligned pattern is one transition canvas per path, each with its own AND-logic trigger conditions."* The engine validator's ban on OR-logic in stage_helpers forced the two-canvas pattern; the narrative moment (Jake notices Maya passing his door) is one beat, so the prose is one beat.

The valid shape requires:

- A comment at the file location naming the engine constraint
- Each duplicate references the same mechanical-route variant (different trigger conditions, identical body)
- Quest card pointer (R3) points at ONE of the duplicates — usually the more predictable trigger — per the convention in J1's card (`ready_canvas = "transition_jake_to_1_via_beauty"`)

Do NOT collapse to single-canvas if the engine constraint is real. Do NOT diverge the prose to fake distinct beats — that turns the mechanical split into a fictional inconsistency. The mechanism is the duplication; the fiction is the single beat.

---

## §10 — Open questions / scoped-out

Things this doc deliberately does NOT cover:

- **Cross-NPC arc transfer mechanics.** RTS `SellingMyStepsister` transfers Brother's arc into Josh's. TLS currently has no equivalent. Whether to add cross-NPC transfers (and where they'd fit doctrinally) is a future design decision. The mechanism would be a Type B Accept-path that sets a flag activating another NPC's chain — engine already supports it; doctrine doesn't currently endorse it.
- **Pregnancy capstones.** RTS has variant pregnancy passages (e.g., `BrotherBedroomPregnantSex1`). TLS currently has none. Per Doc 30 §7.3.1, the slice ships bareback for retrofit compatibility. When pregnancy retrofit happens, capstone variants per pregnancy state are a new category — doctrine writeup needed at that time.
- **Capstone replay / gallery mode.** RTS has `galleryMode()` which lets the player re-watch unlocked scenes. TLS Quests V2 doesn't have a gallery surface. Future Phase 2+ engine work per Doc 34 E10e.
- **Capstone weight in pacing.** How many capstones should fire across a given in-game week? If a Type C chain has 5 capstones and the player triggers them all in 3 days, the arc feels rushed. RTS gates this via cumulative trait requirements (each capstone needs the next stat tier). TLS uses the same pattern; whether the absolute pacing reads right is a playtest question, not a doctrine question.
- **Voice authoring guide for Tier-3 prose.** Doc 56 R2 + this doc §6 name the register. Concrete guidance on HOW to write Tier-3 prose (rhythm, specificity, restraint) is its own future doc if it becomes load-bearing.
- **Capstone visibility in published catalog.** When the catalog UI ships (per Doc 56 P2 alignment), capstones should display alongside Lane 1/2/3 scenes with their requirements + GUIDE text. RTS already does this. The doctrine for *which* capstones appear (all? only completed? only those quest-card-pointed?) is its own decision.

---

## §11 — References

### Sibling and ancestor docs

- **Doc 24** — 3 Lanes + TLS Engine Fitness. §10.8.C named capstones as out-of-scope-for-3-lanes; this doc fills that gap.
- **Doc 30** — TLS Test Redesign PRD. The 6-NPC roster + per-arc vocabulary ceilings inform per-NPC capstone budgets in §5.
- **Doc 31** — Frank Arc Design Brief. The gold-standard Type C chain reference (Frank's 5 capstones).
- **Doc 50** — Quest Card Shape Doctrine. R1 (capstone coverage) and R4 (chain continuity) are restated here as R3/R4. R6 in Doc 56 (no `txt_only` cards) ensures capstones have card pointers.
- **Doc 53** — Marge Redesign Brief. The service-NPC adaptation with `canvas_marge_interview` as the sole capstone — exemplary Type A for service register.
- **Doc 54** — Marge Session Lessons. The 27 failure modes catalog. Capstone authoring is touched in §3 (design failures).
- **Doc 56** — RTS Principles & TLS Alignment. P3 (one scene, multiple lengths) and P8 (author points of no return; mechanize the texture) inform §6 voice and §3 type taxonomy.

### Memory entries

- `rts_three_lanes_lane3_design` — Doc 24 the lane mechanism this doc extends
- `rts_state_variant_authored_vs_mechanism` — Doc 35; capstones are the "authored" half of that doctrine
- `feedback_tls_scene_body_style` — Lane 2/3 voice doctrine; this doc names where Tier-3 register is allowed (capstones only)
- `doc-56-rts-alignment-doctrine` — sibling doc, the 10 principles + 7 rules + per-arc-shape distribution

### Live TLS reference (verified during session)

- `games/the_long_summer_test/toml_phases/7_final_game.toml:1603` — `canvas_marge_interview` (Type A worked example)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:3320` — `scene_franks_bedroom_evening` (Type B worked example)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:7416` — `scene_frank_declaration` (Type A, Type C step)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:7778` — `scene_ryan_first_date` (Type A)
- Frank chain anchors (Type C chain): `scene_livingroom_catch` → `scene_franks_bedroom_evening` → `scene_frank_declaration` → `scene_frank_sleepover` → `scene_diana_confrontation`

### RTS source (verified during session)

- `SellingMyStepsister` (`passage_catalog.json`, 7,837ch) — Type B canonical, cross-NPC transfer
- `VeronicaMeet` (10,602ch) — Type A canonical, peer/intro first-meet
- `MarcusParkSex` (4,900ch) — Type A in a Type C chain (Marcus arc step)
- `SecretAdmirer` (7,927ch) — Type A career-arc starter

### Engine primitives

- `selectAutoFireCanvasForLocation` (`v1.py:3236`) — the engine entry point that fires capstones on location entry
- `triggerConditionsSatisfied` (`v1.py:2684–2952`) — predicate evaluation for capstone gates
- `markCanvasTriggered` — sets the `trigger_history` flag so the capstone retires after firing

---

## Appendix A — Pre-ship checklist for capstones

Copy this into a PR description (or run it mentally) before merging any capstone:

**Trigger fingerprint:**
- [ ] **R1** `is_repeatable = false` (or equivalent flag-gate in conditions)
- [ ] **R1** `trigger_mode = "manual"` (default)
- [ ] **R1** `priority ≥ 9`
- [ ] **R1** `conditions` include the flag-is_false gate preventing re-fire
- [ ] **R1** Exit choice sets the corresponding setter flag via `flagEffects`

**Type classification:**
- [ ] Type declared: A / B / C-step. (Doc 57 §3)
- [ ] **R2** If Type B: both branches set different flags OR transfer arcs OR have materially different downstream content
- [ ] **R5** Schedule + location match the fiction; not chosen for engine convenience

**Pattern F (if Type B):**
- [ ] **F1** Both branches playable in good faith
- [ ] **F2** Real divergence in flag-effect or downstream content
- [ ] **F3** Fork at the cascade's terminal beat
- [ ] **F4** Refuse-path flag policy matches fiction (retry-allowed vs irreversible)
- [ ] **F5** Not compounded with tier-routing AND multi-step downstream — only one structural device beyond the fork

**Voice:**
- [ ] **§6** Cascade prose is Tier-3 (specific, layered, character-distinguishing)
- [ ] **§6** No Tier-3 spillage planned for related Lane 2/3 canvases that reference this capstone's content

**Cross-doc compliance:**
- [ ] **R3 / Doc 50 R1** Capstone is referenced by some quest_card's `ready_canvas` OR has `# off-panel:` comment
- [ ] **R4 / Doc 50 R4** If part of a Type C chain, predecessor capstone sets the flag this one requires
- [ ] **Doc 56 R2** T0/T1 endings (if internally-tiered) land on in-fiction interruption — but capstones rarely tier-route; if this one does (e.g., scene_franks_bedroom_evening climax-node corruption < 40 vs ≥ 40), the lower-tier closing reads as a "more would have been here" cue
