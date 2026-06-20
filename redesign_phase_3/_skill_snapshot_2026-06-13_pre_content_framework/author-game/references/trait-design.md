# Designing an NPC's trait spine (which trait drives the arc)

Read this when writing an NPC's R7 stat ladder (setup) or gating its rungs/capstones (continue). The
canonical trait catalog — names, ranges, decay, sidebar — lives in `prompts_v2 doctrine/09`; this file
is the one decision that catalog doesn't make for you: **which trait actually drives THIS arc.**

## The core idea: traits have roles, and the role depends on arc shape
A trait isn't just a number — it carries a meaning, and the meaning a player *feels* differs by arc
type. The failure mode is **gating every NPC on one trait** — and it comes in two flavors, BOTH wrong:
- **`relation`-on-everything** — the lazy default. In RTS `relation` is the *least*-used numeric gate,
  reserved for peer/dating; family arcs run on corruption × NPC willingness with `relation` absent.
- **`corruption`-on-everything** — the subtler, more common trap in a corruption-premise game. Player
  `corruption` is a *global depravity meter*; using it as the gate for every NPC's private milestone
  makes it do double duty as the per-NPC relationship clock too. "I'm not using `relation`" is NOT
  compliance — if a per-NPC milestone gates ONLY on player corruption while the NPC's own built
  **permanent** axis (relation, or the NPC's own corruption) is ignored, you've made corruption the
  universal spine. (Last Call's Marcus is the case: his `relation` climbs all arc but only the *first*
  capstone reads it — the deeper ones switch to player corruption, so the relation you build goes dead.)

**RTS never does this.** Its workhorse NPC-arc gate reads the NPC's *own* two axes, never the player's
corruption (live-verified — `game_explorations/rts-align-verify/notes.md`):
```js
StageOne(npc)   = npc.corruption >= 5  && npc.arousal >= 1
StageTwo(npc)   = npc.corruption >= 10 && npc.arousal >= 2
StageThree(npc) = npc.corruption >= 15 && npc.arousal >= 3
```
Player `corruption` gates a *separate* layer (the depravity tier + public/self-display content), never
a specific NPC's progression. **Note these RTS scenes are REPEATABLE** — that's why the `arousal`
*throttle* can be in the gate (you re-warm him each visit). One-shot milestones are different — see
"Throttle vs odometer" below.

## Pick the SPINE by arc shape
The spine is the trait whose thresholds gate the arc's rungs and capstones. Choose it from the shape:

| Arc shape | Spine (what gates the rungs) | Notes |
|---|---|---|
| **Peer / dating** | `npc.relation` as **small milestones** (5/10/15-ish) | courtship is the bond; `corruption` stays low. A money axis fits sugar/transactional peers. |
| **Family / slow-burn / escalation** | `npc.corruption` (his ODOMETER) + `npc.arousal` (his THROTTLE); player `corruption` = secondary floor on the most explicit beats | the classic burn: build *him* (his corruption) + warm him up (his arousal); her global depravity only floors the explicit scenes. See "Engine spine note". |
| **Leverage / transactional** | `money` / debt + `corruption` | the pressure is economic, not affection — don't gate it on `relation`. |
| **Service** | `npc.relation` (trust) | workplace bond; `arousal`/`corruption` don't apply (empty, per `lanes.md`). |
| **Antagonist / witness** | a hidden `awareness` accumulator | never `relation`; never surfaced (spoils the confrontation). |

### Reserve the RICH two-meter model for the core — most NPCs run LIGHT
The full **odometer + throttle** treatment (the Family/slow-burn row: his `corruption` + his `arousal`)
is **expensive to author and only pays off for the central slow-burn relationship(s).** It is NOT the
default for every NPC. **Verified in RTS:** the two-meter model is used by **only the 3 housemates**;
**every other NPC** (dating, transactional, service, one-off — ~14 of them) gates on **player corruption
+ a flag** (or a single `relation` milestone). So:
- Pick the **1–2 "house core" arcs** that carry the game — give *them* the two-meter model.
- Author **everyone else LIGHT**: one odometer (`relation` or `money`) + flags, or just the player-
  corruption tier + a flag. A peripheral NPC does NOT need its own arousal throttle or corruption odometer.
- Most NPCs stay light regardless of cast size: even a full game keeps most NPCs light (RTS is a full
  game and still reserves the rich model for just 3). Gold-plating every NPC is the failure — it dilutes
  the core and triples the authoring. (`rts-design-philosophy.md` P5.)

Record the chosen spine in the NPC's R7 brief stat ladder so the continue loop gates on it instead of
defaulting to `relation`.

## Throttle vs odometer — the decisive distinction for what gates what
Not all meters are the same KIND, and the kind decides what a meter is allowed to gate:

- **ODOMETER** = permanent, never resets. Player `corruption`, `npc.relation`, `npc.corruption`. This
  is the **spine** — it measures how far the arc has *permanently* come. Odometers gate the permanent
  progression: **escalation rungs AND one-shot capstones**.
- **THROTTLE** = resets (to 0 at climax). `arousal` (player or NPC). It measures "is he/she **in the
  mood right now**." A throttle climbs (daily + per directed act) and resets each climax. A throttle
  gates **repeatable, in-the-moment content** — the sex-loop acts, RTS's repeatable stage scenes —
  where re-warming each session is the intended cadence.

**A throttle must NEVER gate a one-shot capstone.** A one-shot fires once and never re-evaluates; a
permanent milestone (first kiss, first night) can't hinge on a transient state that wipes at climax —
and narratively the "first kiss" is a progression event (how far it's come), not an "is he warmed up
tonight" event. So:

| Content kind | Gate on |
|---|---|
| One-shot capstone (kiss, first night, the date) | **odometer(s) + flags** — never the throttle |
| Escalation rung (locked-visible ladder) | odometer(s) |
| Repeatable in-scene content (sex-loop poses) | odometer (corruption tier) **+** throttle (`arousal`) — re-warm each session |

> **Why RTS "gates scenes on arousal" but our capstones don't:** RTS stage scenes are *repeatable*, so
> the `arousal` throttle in `StageOne(npc)` fits (re-warm per visit). Our one-shot capstones are the
> permanent first-time beats — they gate on the odometer (player `corruption` / `npc.relation`) + the
> flag chain, and the throttle is reserved for the **repeatable sex loop** that follows. Same parts,
> assigned by repeatable-vs-one-shot. (LC Sal: kiss/first-night = corruption + flags; the loop = corruption + `npc_sal.arousal`.)

**Engine spine note — prefer a PER-NPC odometer.** RTS's odometer is the NPC's *own* `corruption`,
raised by the lewd acts you do with him (daily-capped, never resets) — so each arc progresses by what
you build *with that NPC*, not by global sluttiness. **Prefer this:** give the NPC `npc.<id>.corruption`
(declared in core_traits), raise it on his lewd beat (e.g. a Flirt rung, daily-capped via a `_today`
flag in `[engine.daily_tick]`), and gate his milestones on it. Reserve **player `corruption`** as the
*secondary* depravity floor on the **most explicit** beats only (RTS's `requirementsMC` ladder:
~0 for the kiss/grope tier, ~30 for first penetrative sex) — not as the spine of every NPC's arc.
Leaning the whole arc on player `corruption` is the corruption-on-everything trap. (LC Sal: kiss =
`npc_sal.corruption ≥ 3` + flags; first night = `npc_sal.corruption ≥ 5` AND player `corruption ≥ 30`;
his corruption built by his charged beats — `game_explorations/rts-align-verify/notes.md`.)

**How to BUILD the odometer (RTS rule):** raise `npc.<id>.corruption` **+1 from every charged/lewd
beat** with him (flirt, the kiss, grope, sex), each **daily-capped** (a `_today` flag, or a once-only
capstone) — **never from neutral talk** (talk is warmth/arousal only). Use it on *several* beats, not
one, so the odometer climbs as the player escalates and there's no single-rung soft-lock. **One charged
beat moves SEVERAL meters at once** (RTS P7): the same flirt/grope raises his throttle (`arousal`) AND
his odometer (`corruption`), and often her odometer (player `corruption`) too — one click, multi-axis,
so the meters advance together (e.g. LC's "Stay after close" = `npc_sal.arousal +1` AND `npc_sal.corruption +1`). **Don't**
raise it inside an *uncapped repeatable* loop unless a gate reads above the capstone thresholds — an
unbounded climb that gates nothing is worse than skipping it (LC's sex loop deliberately omits it: no
his-corruption gate exists above the first-night value).

### Throttle-keyed PROSE stays heat-framed (transient), never relationship-status
If hub/scene prose varies by the `arousal` throttle, write it as **heat of the moment** ("he's wrung
out tonight" → "he's watching you, not hiding it") — NOT as courtship status ("you're a stranger" →
"you're together"). Relationship status is permanent; it belongs to the odometer/flags. Keying
*status* prose to a resetting throttle makes it **regress after climax** (RTS's own bug-avoidance: it
shows arousal as a neutral heat emoji ❄️→🔥🔥🔥, never status text). This was the real LC Sal defect —
not the gate.

## The three NPC axes have distinct, independent jobs
When an arc uses more than one, keep their jobs separate:
- **`npc.arousal`** = wants-her-*now* — the short-term dial, a **THROTTLE** (resets at climax). Gates
  Lane 2/3 eligibility and **repeatable in-scene content**; never a one-shot capstone (see above).
- **`npc.corruption`** = willing-how-*far* — the long-term willingness ceiling, an **ODOMETER**
  (permanent). Gates rungs + capstones.
- **`npc.relation`** = the *bond* — courtship/commitment beats, an **ODOMETER** (permanent). High-
  relation + low-corruption = chaste mentor; high-corruption + low-relation = FWB. Independent; don't conflate.

## Who initiates the milestone shapes the ODOMETER you pick (not whether to use the throttle)
For an NPC-initiated milestone (a pursuer arc — he kisses her, he asks her out), pick the **odometer**
that matches the fiction — a throttle still never gates a one-shot (above):
- **NPC-initiated dating** (he courts/invites) → odometer = `npc.relation` (the bond). RTS Marcus:
  `relation` builds → he invites → the `boyfriend` flag opens the arc; player corruption never gates
  the courtship, only the explicitness of individual scenes once together (live-verified, notes.md).
- **NPC-initiated seduction** (he makes the first physical move) → odometer = how-far-it's-come
  (player `corruption`, the engine adaptation, **+** the relationship flag chain), NOT the `arousal`
  throttle. His *wanting* is real, but it's the THROTTLE — it gates the repeatable loop after the
  first night, and it colors the hub prose (heat-framed). The one-shot move itself is keyed to the
  odometer + flags (LC Sal: kiss = `corruption` + `sal_opened_up`; the throttle drives the loop). 
- **Player-initiated** (she escalates via Lane 1 clicks) → odometer leads (player `corruption`); same
  rule, throttle stays on repeatable content.

## Player `arousal` is a separate self-meter (not the NPC dial)
Distinct from everything above: **player `arousal`** (0–10) is *her own* per-attempt fuel, not any
NPC's wanting. Climbs +1 per lewd beat and +1/day (no decay), and **resets to 0 only at climax**
(author-emitted — there is no engine macro that zeroes it). It gates *her* lewd actions (must be `>0`
to masturbate; cascade/lewd-menu thresholds), never long-term progression (that's `corruption`). Full
spec: `prompts_v2 doctrine/09 §3.2`. Don't confuse it with the sex-loop's `loop_player_pleasure`, which
is per-scene state (see `sex-loop.md`).

## Anti-pattern: the dead meter
A trait that **climbs but gates nothing** is a bug, not flavor — and it's worse when it's a visible
sidebar bar, because the player reads progress that isn't real (a common miss: an `npc.arousal` or
`exhibitionism` meter that ticks up but no gate ever reads it). Rule: **every trait you raise must
either gate something or be cut.** When you add a `+trait` effect, name what reads it; if nothing does, delete the
effect or add the gate. (Sidebar bars are the loudest offenders — only surface a trait the player can
act on.)

## Slow-burn pacing: earn the willingness, don't tick it
`prompts_v2 doctrine/09` §4.1 sets NPC `arousal` to a passive `+1/day` for in-scope family NPCs
(source: Doc 40) — that's RTS *ambient-family fastness*, which makes the meter hit cap in a few days
no matter what the player does. For a **slow
burn**, that collapses the arc back to one axis. Instead make the willingness axis **earned** from
arc beats (a daily-capped raise on the NPC's daily interaction + specific charged moments), with **no
passive daily climb** for that NPC. That keeps the burn player-driven and paced. Flag it in the brief
as a deliberate deviation from the `doctrine/09` §4.1 default, and reach the cap only through play. (Daily-cap cheaply via the
NPC's existing once-per-day flag, e.g. `talked_to_<npc>_today`, shared across the raise sources.)

## Cross-cutting axes (not per-NPC)
`corruption` (global content tier), `exhibitionism` (public/display — a natural fit for bar/club/
service premises; gate the public floor on it), and `money` are **player-global**, not owned by one
NPC. Use them for premise-wide content (the floor, the shop, the debt), and let the per-NPC spine sit
on top. **Player `corruption` is locked to 0–100, 4 bands (Pure / Lewd / Slutty / Whore)** — author
thresholds on that scale, NOT the RTS 0–200 scale (`doctrine/09` §3.2). Player corruption is the
*global depravity tier*, NOT a per-NPC relationship clock: a specific NPC's milestone gated ONLY on it,
with that NPC's own built axis ignored, is the corruption-as-universal-spine bug (see "The core idea").

## Self-check
- Each NPC's gates use a **shape-appropriate odometer** — not `relation`-on-everything AND not
  `corruption`-on-everything (player corruption is the global depravity tier; an NPC's *permanent* own
  axis, if built, must gate the milestones it earns — see Marcus).
- **Throttle stays off one-shot capstones.** `arousal` (resets at climax) gates repeatable in-scene
  content only; one-shot capstones gate on the odometer(s) + flags. Never gate a permanent milestone
  on a meter that wipes.
- **Throttle-keyed prose is heat-framed/transient** ("in the mood / not"), never relationship-status
  (status belongs to the odometer/flags — else it regresses after climax).
- No **dead meters / split spine** — every raised ODOMETER is read by the milestone it's meant to earn
  (a relation that climbs but only gates capstone #1 is a split spine — Marcus). A throttle read by the
  repeatable loop is correctly used, not dead.
- Slow-burn willingness is **earned + daily-capped**, not passive.
- Every spine/loop trait is **declared before use** in `[player.core_traits]` / `[npcs.core_traits]` —
  an undeclared trait is a silent no-op gate (`doctrine/09` §2, `toml-gotchas.md`).
- Trait names/ranges/decay match `prompts_v2 doctrine/09` (don't reinvent the catalog).
