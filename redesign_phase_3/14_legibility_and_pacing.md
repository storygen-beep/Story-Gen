# Legibility (Gap 3) + Pacing (Gap 4) — finishing the desire-ladder experience

The last two dry-run gaps (`08`). Both are small *because the desire ladder (`09`) + economy (`13`)
already carry most of the work* — but designed properly here. Gap 3 = the player always knows what to do.
Gap 4 = the game has a good rhythm. They reinforce each other (the visible next-want IS the always-near
next-payoff).

---

# PART A — Legibility (Gap 3)

## The honest framing
We already HAVE the surface (quest cards / the V2 quests engine, Doc 49). **RTS also has a tracker and
STILL got "I don't know what to do."** So Gap 3 is **not "build a tracker" — it's a discipline on the one
we have**, so it actually delivers. Two failures to kill:

## The rules
- **L1 — The tracker IS the desire ladder, surfaced.** The top "Story Goals" card always shows the
  **current want** (the active rung of the desire ladder `09`) as ONE coherent thread — not scattered
  per-NPC cards with no spine. (Reuse: the no-`npc_id` quest card = the "Story Goals" section.)
- **L2 — Show the next ACTION, not just the goal.** Each active card shows the want **+ the next concrete
  step (what · where · when)** — "Make rent ($X) — work the floor for tips, evenings," not just "make
  rent." This is the exact RTS failure (the guide named the goal, not the step). (Reuse: the card
  `text`/`tip`/`goals` fields carry the action.)
- **L3 — Telegraph what's coming.** The next want/rung is visible ahead (greyed/locked-visible), so the
  player sees where they're headed. (Reuse: locked-visible rungs `lanes.md` + the quest chain showing the next stage.)
- **L4 — Never stale.** Exactly one current want shown; it retires and the next appears as wants clear.
  (Reuse: the milestone-chain `when`-gating pattern — one card live at a time.)
- **L5 — Per-NPC wants are legible too.** Each NPC you're pursuing shows *its* current want + next action
  in that NPC's quest section (`npc_id` cards). Main thread (the ladder) AND active pursuits are both clear.
- **L6 — The FRONTIER is narrated honestly, never blank** (`17` — endless ≠ aimless, the RTS sin). When the
  player reaches the current top of the ladder, the tracker says so plainly — *"You've reached the current
  peak — run your empire, [the steady-state loop]. More to come."* — instead of going empty. The edge of
  authored content is *told to the player*, with the livable steady-state named, so the open sandbox feels
  like arrival, not "I don't know what to do."

## Anti-patterns
- A card that names only the abstract goal ("seduce Sal") with no action.
- Scattered/stale cards with no single "what you're chasing now."
- The player ever staring at the screen not knowing what to do (the RTS sin).

## Check
At any moment, the tracker names the **current want + the next concrete action**; the next want is
visible ahead; no stale cards; both the main ladder and each active NPC pursuit are legible.

---

# PART B — Pacing (Gap 4)

## The principle
The game is a **curve of tension → release, escalating** — never flat grind, never all-at-once. The
desire ladder gives the rhythm (chase → clear = payoff → new want); the economy gives the escalation
(dirtier/better as you climb). Gap 4 designs the *curve* + sets the *rates*.

## The rules
- **P1 — Every want is a tension→release unit.** A want = a few buildup beats (pursuit) → a **PAYOFF
  scene** when cleared (`09` R5). The game is a sequence of mini-arcs, each ending in a payoff. **No want
  without a payoff.**
- **P2 — Escalate across wants, then PLATEAU (climb → plateau → climb).** Each payoff is hotter/bigger than
  the last — stakes, explicitness, and reward climb (the heat curve rises) **up to the frontier** (`17`).
  Escalation isn't infinite (you can't get endlessly more explicit/powerful): at the current top rung the
  curve flattens into a **wide, livable plateau** (the steady-state sandbox), and a later extension *lifts*
  the plateau to a new height. So: steep climb up the authored ladder → sustainable plateau at the top →
  climb again when extended. (Ties to the cascade acts `04` + economy tiers `13` + the frontier `17`.)
- **P3 — Alternate big and small.** Mix major payoffs (first night, taking the bar) with lighter beats
  (small wins, ambient reactivity) — not all peaks (exhausting), not all valley (grind). Small wins
  *building to* big payoffs.
- **P4 — Cap the gap between payoffs (anti-grind).** Never a long stretch with nothing landing. There's
  always a **near payoff, visible and reachable** (this is where Gap 3's legibility = Gap 4's "next payoff
  is close" — same thing). If the player does many beats with nothing paying off, pacing is broken.
- **P5 — Don't dump it all at once.** The opposite failure — gate the big content so it's *earned*; the
  kiss / first night / the bar are spaced as peaks, not handed over early. (The double-lock + cascade
  tiers `04` already enforce this spacing.)
- **P6 — Rates are authored PER GAME (no hardcode).** The principle (P1–P5) is fixed; the **numbers** are
  tuned at generation so the climb feels *earned but not grindy.* The pacing knobs to tune:
  - meter **climb rate** (per charged beat / per day),
  - **beats-per-want** (how much pursuit before a payoff),
  - **payoff frequency** (the cap from P4),
  - **escalation steepness** (how fast heat/stakes rise),
  - the **rent/debt deadline cadence** (the pressure clock `13`).
  Tuning these = tuning the pacing.
- **P7 — The ENDGAME escalates in CONTENT, never into management** (`15` Finding C — the biggest). The mirror of
  LC's failure: LC was a grind *up to nothing*; an empire/endgame fantasy fails the *opposite* way — it
  **drains down into a spreadsheet** (recruit girls = +income, upgrade the place = stat bumps, "become the
  madam" = a dashboard), so the heat thins exactly when the player is most powerful. **Forbidden:** an endgame
  whose escalation is administrative. **Required:** every empire/endgame beat cashes out as *content* —
  - each **recruit is a full corruption arc** (a `07` NPC with her own double-lock + capstone + loop — `13` E9), never a +income unit;
  - **"upgrading" unlocks new KINDS of scenes** (the back room becomes a play space), never a number going up;
  - the **madam/apex endgame is the HOTTEST beats** — she *uses* the stable, directs/commands the content, is the apex of it — not a manager *of* it.
  The peak of the game must be the peak of the *content*, not the start of the bookkeeping.

## Anti-patterns
- **Flat grind** — a long stretch, no payoff (P4 violated).
- **Front-loaded dump** — the big content given early (P5 violated).
- **Metronomic** — same rhythm forever, no escalation (P2 violated).
- **Payoff-starved want** — a want that doesn't end in a payoff (P1 violated).
- **Management drift** — the endgame escalates into admin/spreadsheet, heat thins at the top (P7 violated).

## Check
Every want ends in a payoff (P1); payoffs escalate (P2); big & small alternate (P3); no long gap between
payoffs (P4); big content is spaced/earned, not dumped (P5); rates authored per game and tuned for
earned-not-grindy (P6); the endgame escalates in CONTENT not management — recruits are arcs, upgrades unlock
scenes, the apex is the hottest beats (P7).

---

## How A & B reinforce
Legibility (you always *see* the next want) and pacing (a payoff always *lands* soon) are the same coin:
the visible next-want (L3) is the always-near next-payoff (P4). Together they make the desire ladder
*feel* like a game with momentum, not a meter to fill.

## Engine / skill reuse (implementation, later)
- **Gap 3:** quest cards / V2 quests engine (Doc 49), milestone-chain `when`-gating (one card live),
  locked-visible rungs (`lanes.md`). No new system — a usage discipline (L1–L5).
- **Gap 4:** meter climb rates (`[engine.daily_tick]` + per-beat effects), the cascade tiers + double-lock
  (spacing, `04`), capstones (the big payoffs), the rent cadence (`13`). Pacing = *tuning these per game*
  to P1–P6.

## Cross-references
- `08` Gaps 3 & 4 · `09` desire ladder (the wants/payoffs these surface & pace) · `13` economy (the rent
  cadence + tiered pay) · `04` cascade (the spacing) · `05` quality #2 (legible pull), #4 (payoff), #6 (pacing).
