# RTS design philosophy — the WHY behind the trait/progression model

The "why" companion to `trait-design.md` (the "how"). Extracted from RTS ("Road to Success") by direct
source + runtime verification this session — evidence in `game_explorations/rts-align-verify/notes.md`
and RTS's OWN in-game `GameMechanics` page. Each principle separates **VERIFIED** (mechanic / RTS's
own words) from **INFERRED** (the design intent behind it — RTS may not have articulated it, but the
observable logic is consistent). Read this to understand the model; read `trait-design.md` to apply it.

> RTS, in its own words (GameMechanics page): *"The available actions and scenes depend on your
> corruption level. You start at the 'Pure' stage. Your stage evolves—unlocking new actions and
> scenes."* and, under **House Events**: *"Household events involving your housemates are influenced by
> **their arousal levels and your corruption** … the higher the arousal, the further the events
> progress. Corruption also plays a significant role."*

---

## P1 — Player corruption is the master CONTENT-TIER, not a relationship clock
**Verified:** `getCorruptionLevel()` bands (Pure→…); GameMechanics says actions/scenes depend on it;
nearly every scene carries a `requirementsMC.corruption`.
**Intent:** one global axis answers *"how far will SHE go?"* — it tiers **what kind of content exists
at all** across the whole game (a depravity ceiling on the player). It is NOT a measure of any one
relationship. Using it as the per-relationship progression is the **corruption-on-everything trap**;
RTS keeps relationship progression on per-NPC / flag axes instead.
*(Variant: the master tier can be **dead** when the player is a **still-point** — a honeypot / owned weapon whose
own corruption never climbs; then both axes live on the NPC. See `trait-design.md`'s honeypot row + `content-framework.md §1B`.)*

## P2 — Two KINDS of meter: ODOMETER (permanent) vs THROTTLE (resets)
**Verified:** `arousal` resets to 0 at climax (`finishSex`→`ResetArousal`); `corruption`/`relation`
never reset; **no decay anywhere** in the engine.
**Intent:** an **odometer** tracks irreversible progress (lines crossed that can't be uncrossed); a
**throttle** tracks transient readiness ("in the mood now") and forces re-engagement each session.
Different jobs — they can't be collapsed onto one number. (This is THE distinction that drove most of
this session's corrections.)

## P3 — The core gate is two-axis: HIS state AND HER state
**Verified:** GameMechanics House Events ("their arousal levels and your corruption");
`StageOne/Two/ThreeCorruption(npc) = npc.corruption ≥ 5/10/15 AND npc.arousal ≥ 1/2/3`; runtime-proven
neither axis alone unlocks. Scenes carry `requirements` (the NPC's own axes) AND `requirementsMC` (the
player's).
**Intent:** content unlocks at the **intersection** of "how far HE's come" and "how far SHE'll go" —
a two-sided relationship. One party's state alone is never sufficient.
*(Variant — the double-lock **on the NPC**: when the player is a still-point, BOTH axes can be the NPC's own
(`relation` = access + `corruption` = willingness), with no player floor. Same two-sided intersection, both sides HIS.)*

## P4 — Per-NPC odometers: each arc progresses on what you build WITH THAT PERSON
**Verified:** each family NPC has its OWN `corruption`; `StageN` reads `npc.corruption`, never the
player's.
**Intent:** arcs feel individual. You can't unlock one person by grinding another, or by being globally
slutty. The per-NPC odometer is the concrete device that PREVENTS corruption-on-everything (P1).

## P5 — Reserve the rich model for the CORE; peripheral arcs run light  ← the non-naive one
**Verified (survey of all NPC scene-gates):** only **Dad / Brother / Grandpa** (the housemates) use the
full `npc.arousal` + `npc.corruption` two-meter model. **Every other NPC** — Marcus, Veronica, Edward,
Priest, Landlord, Emma, Sam, … — gates on **player corruption + flags** (and, for dating, a
button-level `relation`/`boyfriend` flag), with their own scene-`requirements` axes empty. RTS's
GameMechanics scopes the two-axis statement explicitly to "housemates."
**Intent:** the odometer+throttle pair is **expensive to author** and only pays off for the **central
slow-burn relationships**. Peripheral / transactional / one-off NPCs use the **cheapest gate that
works** (the global corruption tier + one flag or a relation milestone). **Do not gold-plate every
NPC.** Pick which 1–2 arcs are the "house core" and lavish the two-meter model there; keep the rest light.

## P6 — The throttle gates REPEATABLE content and re-warms each session
**Verified:** arousal climbs (+1/day passive for family, +1 per directed act), resets at climax, and
gates the **repeatable** stage scenes; "the higher the arousal, the further the events progress."
**Intent:** for content you do REPEATEDLY (the sex acts), a resetting throttle makes each session a
ritual — warm him up, go a little further — instead of a one-time unlock that trivializes every repeat.
The reset is the point: it's what makes you re-engage.

## P7 — One act advances MULTIPLE meters at once
**Verified:** a single tease fires `AddBrotherArousal` (throttle +1) AND `AddBrotherCorruption`
(odometer +1); some lewd scenes also `AddCorruption` (player +1).
**Intent:** every interaction does multi-axis work — warms him *now*, corrupts him *permanently*, and
sometimes corrupts *her* — so each click is meaningful on several axes and the meters move together
coherently rather than needing separate grinds.

## P8 — Escalation is PACED, not rushable: uniform small steps, daily-capped
**Verified:** raises are **+1, uniform** (never scaled by act depth); each scene is `executedToday`-
capped (once/day); arousal's passive bump is +1/day.
**Intent:** you can't spam a meter to max in one sitting. Progress accrues over in-game **days** — the
slow burn is enforced by the **cadence**, not only by the size of thresholds. (Deeper content is gated
by higher thresholds, i.e. more days, not by bigger per-act jumps.)
**How to throttle a repeatable rung** — the concrete menu (threshold spacing / a window-sized time cost / a
counted daily cap / a conditional energy cost, and why one removable flag is brittle) is in
`references/trait-design.md` "Slow-burn pacing".

## P9 — Early intimacy is CHEAP; the global tier only bites at the DEEP/PUBLIC end
**Verified:** the `requirementsMC.corruption` ladder — grope **0**, tease/flash **5**, peep **15**,
first penetrative sex **30**, public jogging-sex **45**.
**Intent:** you can START a relationship's physical arc at low global corruption (it's gated by HIS
state, P3/P4); the player's global depravity only **floors the most extreme content** (penetrative,
public). So per-NPC arcs are NOT grind-gated early — the grind gates only the far end.

## P10 — Surface meters honestly + legibly; match PROSE register to the meter's kind
**Verified:** arousal renders as a neutral heat emoji (❄️→🔥→🔥🔥→🔥🔥🔥); the walkthrough pre-declares
every scene's requirements; arousal-conditional narrative is heat-framed ("he's not in the mood"),
never relationship-status.
**Intent:** the player can SEE state + requirements → **planful** play, not blind guessing. And the
framing must match the meter KIND: a **throttle** is shown/narrated as **transient heat**, never as
permanent relationship status — because it resets, so status prose keyed to it would **regress after
climax**. Permanent status lives in the odometer / unlocked content / flags.

## P11 — Not everything is stat-gated
**Verified:** some scenes (Gangster, Thief, kidnap-type) carry no stat requirement at all — pure
narrative/event/flag triggers.
**Intent:** stats gate the **earned escalation**; **story flags** gate the **scripted turns** (forced
events, plot beats). Don't try to put a stat on everything.

---

## How LC deliberately DIVERGES from RTS (and why it's still faithful)
Being non-naive: LC is not a byte-clone. The divergences are intentional, each preserving a principle:
- **Player corruption as an odometer.** RTS's core odometer is the NPC's OWN corruption; LC *also* uses
  **player corruption** as an odometer (the depravity tier). For LC's core arc (Sal) we additionally
  gave him his **own** `npc_sal.corruption` (adopting RTS's family richness, P4), with player corruption
  as the **secondary floor** on the most explicit beat (P9). Both are valid odometers; the invariant
  (P2/P3) holds.
- **Earned arousal, not passive.** RTS family arousal auto-climbs +1/day ("ambient fast"). LC makes it
  **earned** (Talk/Stay/Flirt) for a player-driven slow burn — a deliberate pacing deviation, flagged
  as such. Still a throttle (P2/P6).
- **One-shot capstones drop the throttle.** RTS stage scenes are *repeatable*, so the throttle is in
  their gate (P6). LC's kiss/first-night are *one-shot* permanent milestones → they gate on the
  **odometer + flags** only; the throttle lives on LC's **repeatable sex loop** (matching RTS's
  repeatable scenes). Same principle, adapted to one-shot structure.
- **Archetype scoping (P5) applied.** Sal = the "house core" → full two-meter model. Marcus (dating) →
  `relation` + flags. Dee (transactional) → `relation`/`money` + corruption. Mirrors RTS giving the
  rich model only to housemates.

## Verified vs inferred — read honestly
- **Verified** (cite freely): every mechanic above + RTS's GameMechanics statements + the axis-by-NPC
  survey. These are observed in source/runtime, not assumed.
- **Inferred** (the "Intent" lines): the design *reasoning*. RTS ships no design doc; the intent is
  reconstructed from consistent observable behavior. High-confidence (the mechanics are too coherent to
  be accidental) but it's interpretation, not RTS's stated rationale — except P1/P3 which RTS states
  outright in GameMechanics.

## Cross-refs
`trait-design.md` (apply this), `lanes.md` (capstone gating), `beat-authoring.md` (the self-audit),
`game_explorations/rts-align-verify/notes.md` (raw evidence), memory `[[rts_arousal_system]]`.
