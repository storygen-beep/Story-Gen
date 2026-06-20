# Last Call — Design Book

*Intent record. Authored at setup by `/author-game`, brought up to the aligned skill 2026-06-03
(R7 briefs added, arc shapes/budgets corrected). Stable; amend explicitly.*

**`scope_mode: full_game`** — the complete game (full per-shape budgets per `doctrine/03` §2; all
five NPCs to full arcs; capstone chains). **Authored so far:** beats 1 (first night), 2 (Sal on-ramp),
9 (shark reveal), 15 (work/earning loop) are validated; the remaining 11 roadmap beats are `planned`.
This book describes the COMPLETE arcs (full_game §1 end-states); the build is honestly in progress.

---

## §1 World Setup

### Premise
Nina (default name; customizable) inherits **The Last Call**, her late uncle Sully's failing dive
bar, plus the debt he owed **Mr. Boyd**, who owns the block. Boyd's enforcer — **the Collector** —
comes every Monday for **$200**. Keep the lights on and the payment made, or lose the only thing
she has left. Tending bar is the one thing she knows how to do.

### Player character
Female, mid-thirties. Inherited the bar + the debt. RTS-shape protagonist: corruption /
exhibitionism / arousal / beauty meters; customizable name, build, look.

### Economic engine
The debt is the engine's **rent system** (`[settings.rent]`): a weekly **$200** payment, due
**Monday**, collected by `npc_collector`. Armed after the first night (`start_after_flag =
debt_explained`). `eviction_mode = flag_set` → missing it past grace sets `bar_seized` and opens a
leverage path rather than ending the game. The player earns via the **Work a shift** solo activity
(`canvas_work_shift`) and deposits/pays at the bank.

### Time model + day-cycle
Standard period model. `starting_hour = 18` (evening), Monday, week 1. Bar-centric — arcs weighted
to Evening/Night; the bar's NPC schedules run 17:00–02:00.

**Day-cycle (the Day System, `doctrine/04` §10).** Night-centric loop: work the bar past midnight
(`canvas_work_shift` advances 120–180 min/turn) → crash upstairs → **`canvas_sleep`** (the router:
solo at `loc_apartment`, gated 00:00–14:00, +540 min jump to mid-morning + energy +75) → wake into
daytime, where the town is open and **Dee stands the depot 10:00–17:00**. The sleep router is what
makes that daytime presence reachable at all — without it the depot window is dead (the Dee-bug law,
`doctrine/04` §10.3). No hygiene cost on sleep: Last Call has no shower activity yet and hygiene
already drains via the daily tick, so a sleep penalty would spiral it.

**Offscreen presence (3rd location category, `doctrine/10` §5.5).** Each arc NPC carries an
`offscreen = true` "away" home so their day is complete on the Schedule page without manufacturing
dead presence: Sal → `loc_sal_place` (home off the clock 02:00–17:00), Marcus → `loc_marcus_place`
("Uptown" 23:00–20:00), Rosa → `loc_rosa_place` (home with family 23:00–17:00), Dee →
`loc_dee_place` ("Across the river," weekday off-hours 17:00–10:00). These are non-navigable labels —
no nav card, no hub, exempt from the presence floor. The Collector is event-only (no away block —
he's a scripted antagonist, not a hangout target).

### Content ceiling
Standard RTS, **default-to-maximum-explicit** (`doctrine/08` §3). Per-NPC ceilings declared in each
R7 brief §2. Corruption + exhibitionism (serve-in-less for takings), transactional favors, coercive
leverage. All sex bareback (Phase-2+ pregnancy-retrofit compatible — no contraception language).

### Phase 2+ decisions (Doc 65)
All four (pregnancy / scandal / gallery / tracker) currently **deferred**. At full_game these are LO's
to resolve via the Stage-1 Q&A when the arcs reach that depth; if any is later set to `include`, the
brief must name its mechanization (setter/owner/threshold) per `stages/01` §0.5.2.

## §2 Locations
**Building** (root `loc_bar` = player start): `loc_bar` (floor) · `loc_kitchen` · `loc_office` ·
`loc_cellar` · `loc_apartment` (home hub + wardrobe). **Town** (via `loc_street`): `loc_bank` ·
`loc_shop` (clothing) · `loc_wholesaler` (Dee's depot). **`loc_shark`** (Boyd's place) — locked,
revealed at beat 9 (unlock contract Case A). **Offscreen** (`offscreen = true`, non-navigable away
labels for NPC home/sleep blocks): `loc_sal_place` · `loc_marcus_place` · `loc_rosa_place` ·
`loc_dee_place` — see the day-cycle note in §1.

Exposure tiers: `loc_bar` during service = **public** (deniable acts only); the bar **after close /
empty** = **private** (full ladder); `loc_office`/`loc_cellar`/`loc_apartment`/`loc_shark` back-room
= **semi-private→private**; town = public.

---

# Per-NPC R7 briefs

## Sal — `npc_sal` (slow-burn)
**scope_mode: full_game.** Ceiling: **explicit** (older-man / competence / earned-loyalty register).

### §1 End-state fantasy
Sal stops being Sully's loyal bartender and becomes *hers* — the man who'd burn the place down before
he let Boyd take it, who locks the door after close and doesn't go home. The end-state is the
after-hours bar with the lights off: him pouring two, her on the wrong side of the bar, the slow
graduation from "Sully's niece" to the only person he answers to. Signature scenes: the first night
he stays past lockup; the first time she's behind the bar *with* him instead of being shown it; the
after-close kiss; the first night upstairs.

### §2 Voice spec
- **Background:** late 50s, poured for Sully thirty years, nowhere else to be, loyal to the bar more
  than to any owner until she earns it.
- **Speech patterns:** terse declaratives; working-class cadence; dry, never effusive; states facts,
  not feelings ("Same Friday next week." not "I'm proud of you"). Compliments are oblique ("Huh.
  You've done this.").
- **Voice samples per stage:** S0 "You'd be Sully's niece." · S1 "Sully never let me close alone.
  Funny." · S2 (close quarters) "Lock the door. We're done for the night." · S3/4 (earned) "Go up.
  I'll kill the lights." — register stays terse even at intimacy; warmth shows in what he *does*.
- **Framing rules:** older-man / steady-hand / earned-intimacy. Crude only once cracked (Tier 4+:
  direct anatomical, but still few words).
- **BANNED:** monologuing feelings; "gruff exterior, soft heart" narration; calling her "kid" after
  S2; purple tenderness.

### §3 Stat ladder (5 tiers; corruption floor × his arousal — the slow-burn axis)
His arousal (`npc_sal.arousal` 0–3) is the slow-burn meter — *earned* from Sal-directed beats
(talk/stay-after-close), never a passive daily climb. Player corruption is the floor that unlocks
her own brazenness (flirt, then sex). No relation gate anywhere in his arc.
| Tier | Gate | Register |
|---|---|---|
| 0 | corruption 0 · his arousal 0 | sizes her up; work talk only |
| 1 | `sal_opened_up` | warms; personal asides |
| 2 | corruption 15 (flirt rung) | flirt; her brazenness shows, his wanting starts to climb |
| 3 | corruption 20 + his arousal 2 + after-close | after-hours; first kiss (`sal_after_hours_done`) |
| 4 | corruption 30 + his arousal 3 + first night | upstairs; explicit, terse-crude — sets `sal_first_done` + `sal_cracked` |

### §4 Per-rung pretexts (sample)
T1: teach-the-regulars / Sully stories. T2: restock together, hands brush; flirt over a busted tap.
T3: counting the till after close; he stays. T4: first night upstairs. T5: he stops going home.

### §5 Lane map
| Location | Window | Exposure | Surfaces |
|---|---|---|---|
| `loc_bar` (service) | 17:00–22:00 | public | Lane 1 hub `canvas_sal_hub` — talk + locked-visible flirt (corr 15) |
| `loc_bar` (after close) | 22:00–02:00 | private | hub escalation rungs (kiss/upstairs) at higher tiers |
L1 rungs: 3 · L2 ambient: 1 (Sal mid-task on entry) · L3: 0 (deferred) · capstones: 3.

### §6 Capstones (3)
1. **First real shift with Sal** (A) — sets `sal_opened_up` *(authored: `canvas_sal_ropes_first`)*.
2. **After-close, he stays** (A) — first kiss; sets `sal_after_hours_done` *(`canvas_sal_after_hours`)*.
3. **First night upstairs** (B, retry-on-refuse) — sets `sal_first_done` **and `sal_cracked`** (the old
   standalone "backbone" capstone is folded in here — the first night *is* the point of no return)
   *(`canvas_sal_upstairs`)*.

### §7 Anti-patterns
❌ Sal narrating his feelings. ❌ "gruff but secretly soft" narrator gloss. ❌ flirt rung visible
before corr 15 unlocked (keep locked-visible). ❌ pet-name "kid" past S2. ❌ Tier-3 prose on the
repeatable hub base (flat — see `canvas_sal_hub`). ❌ Sal sexual before his arousal earns it (the
slow-burn axis). ❌ him at a location his schedule doesn't cover. ❌ effusive/long Sal lines.

### §8 Cross-arc
WRITES: `npc_sal.arousal` (his wanting — the slow-burn axis, earned from Sal-directed beats; no
passive daily climb); `sal_*` stage flags; `corruption +1` on flirt+. READS: `bar_seized` (if the
bar's in jeopardy, Sal's lines harden); player `corruption` gates the flirt rung + both sex capstones.

### §9 Cross-references
Arc shape slow-burn (`doctrine/03`); lanes + per-shape budget (`lanes.md`); capstone + Pattern-F
fork rules (`doctrine/04` §4 — the first night is the Type-B retry); spine doctrine `trait-design.md`
(slow-burn = player corruption × NPC arousal); sex-loop shape `sex-loop.md` (beat_0022). Sibling:
**Rosa** (warns about the men circling — Sal reads as the "safe" one against that backdrop). Canvases:
`canvas_sal_ropes_first`, `canvas_sal_hub`, `canvas_sal_afterhours_hub`, `canvas_sal_after_hours`,
`canvas_sal_upstairs` + the sex-loop nodes.

### §10 Acceptance criteria (done when)
- All 3 capstones reachable and fire in order: ropes_first → after_hours → upstairs.
- Every Sal gate reads `corruption` × `npc_sal.arousal`; **zero relation** anywhere in his arc.
- Flirt rung locked-visible at corr 15 (public hub); kiss at corr 20 + his arousal 2; first night at
  corr 30 + his arousal 3, setting `sal_first_done` **+** `sal_cracked`.
- `npc_sal.arousal` is *earned* from Sal-directed beats (no passive daily tick) and is the only
  Sal-meter written.
- Sex-loop reachable from the after-close hub; resets loop state on entry/exit.
- Hub bases stay RTS-flat; Tier-3 prose only in the capstones.

---

## Marcus — `npc_marcus` (peer/dating)
**scope_mode: full_game.** Ceiling: **explicit** (transactional / sugar / patient-buyer register).

### §1 End-state fantasy
The moneyed regular who tips like he's buying something — because he is. End-state: a kept
arrangement she walks into with open eyes — his money keeps the bar alive (feeds the debt), his
patience curdles into ownership, and she lets it because the alternative is Boyd. Signature scenes:
the first oversized tip with a condition attached; the back-booth "private" drink; the first time the
money is explicitly for *her*.

### §2 Voice spec
- **Background:** 40s, old money or new money that learned manners, drinks top-shelf alone, never
  rushes.
- **Speech patterns:** smooth, complete sentences; courteous with a floor of steel; makes offers,
  not demands ("Keep the change. We both know it's not for the drink."). Never crude until very late.
- **Samples:** M0 "Same as always. And whatever you're having." · M2 "Sit. Five minutes. The bar can
  survive without you that long." · M3 "I can make Monday stop being a problem. You know what I'd ask."
- **Framing:** transactional-becoming-possessive; generosity as leverage.
- **BANNED:** Marcus as cartoon sleaze; explicit early; impatience (his power is patience).

### §3 Stat ladder (6 tiers; relation + corruption)
T0 polite regular · T1 marcus_noticed (singled out) · T2 corruption 20 (accepts the private drink) ·
T3 corruption 35 + marcus_date_done (the arrangement named) · T4 corruption 50 (kept) · T5 marcus_owns.

### §4 Per-rung pretexts (sample)
T1: the big tip. T2: back-booth drink. T3: the offer (money for Monday). T4: the standing
arrangement. T5: she's his.

### §5 Lane map
| Location | Window | Exposure | Surfaces |
|---|---|---|---|
| `loc_bar` (his end) | 20:00–23:00 | public→semi | Lane 1 hub `canvas_marcus_hub` — talk + locked rungs |
L1: 2 · L2: 1 (he's watching from the end of the bar) · L3: 0 · capstones: 3.

### §6 Capstones (3)
1. **Singled out** (A) — `marcus_noticed`. 2. **The arrangement** (B) — money-for-Monday offer,
accept/refuse fork → `marcus_date_done`. 3. **Kept** (A) — `marcus_first_done`.

### §7 Anti-patterns
❌ cartoon-sleaze Marcus. ❌ impatience. ❌ crude before T4. ❌ the offer free of cost/consequence.
❌ him present outside 20:00–23:00. ❌ Tier-3 on the repeatable hub. ❌ his money with no debt tie-in.
❌ forgetting he's a *choice* she makes (no railroad).

### §8 Cross-arc
WRITES: `npc_marcus.relation`, `corruption`, `money` (his tips/payments feed the debt goal),
`marcus_*` flags. READS: `bar_seized` / debt pressure (sharpens his offer); `exhibitionism`
(dress-for-tips raises his attention).

### §9 Cross-references
Arc shape peer/dating (`doctrine/03`); relation-milestone spine (`trait-design.md` peer/dating);
capstone + Pattern-F rules (`doctrine/04` §4 — the arrangement is the Type-B fork); economic engine
(§1 — his money feeds the central debt). Sibling: **Collector** (Marcus's clean money is the
alternative to the Collector's leverage — two routes to "Monday handled"); **Rosa** warns about him.
Canvases: `canvas_marcus_hub`, `canvas_marcus_singled_out`, `canvas_marcus_arrangement`, `canvas_marcus_kept`.

### §10 Acceptance criteria (done when)
- All 3 capstones reachable in order: singled_out → arrangement → kept.
- Entry on `npc_marcus.relation` (≥ 15); escalation on `corruption` (35 arrangement, 50 kept) + flags.
- His payments add `money` that can clear a Monday — the debt tie-in is present, never free.
- The arrangement is a real accept/refuse fork (refuse re-offers, no penalty); "kept" is a choice, no railroad.
- Quest-card corruption goals labelled "My corruption".
- Hub stays flat; Tier-3 prose only in the capstones.

---

## The Collector — `npc_collector` (antagonist)
**scope_mode: full_game.** Ceiling: **explicit** (coercion / dubcon-framing register).

### §1 End-state fantasy
The debt with a face. He starts as a weekly knock and becomes the coercion engine — when the money
comes up short, "money's one way to keep a roof over your head; there's others." End-state branches:
she pays her way out (clean), or the leverage path takes over (favors instead of cash) and culminates
in a confrontation with Boyd. Antagonist shape: a **debt-enforcer** — he escalates on player
`corruption` × the `bar_seized` economic flag (NOT an awareness meter; that's the witness sub-type /
Diana model), not a romance she pursues. Signature scenes: the first short week; the summons to Boyd;
the leverage turn.

### §2 Voice spec
- **Background:** heavyset, unhurried, "Reggie when he's friendly, which is never twice"; works for
  Boyd, who owns the debt and the block.
- **Speech patterns:** flat, economical, menace without volume; states terms like weather ("One week.
  I'm not a bank and I'm not your friend."). Never threatens explicitly — implies.
- **Samples:** C0 "Two hundred. You got it, or you got a story?" · C-leverage "Money's one way. There's
  others. We'll talk about what works for me." · Boyd "I have ways of being paid that don't involve
  money. Are we understanding each other?"
- **Framing:** coercive, transactional, deniable; the threat is in the quiet.
- **BANNED:** ranting/yelling; explicit threats of violence (he implies); him as seducible/romanceable;
  comic-menace.

### §3 Leverage ladder (antagonist / debt-enforcer — no romance tiers; flag + corruption gated, NO awareness trait)
L0 collecting (on time) · L1 short week (`rent_warned`) · L2 behind (`bar_seized`) → leverage offered
(register hardens on player `corruption`) · L3 summoned (`summoned_by_shark`) → Boyd · L4 confrontation/resolution.

### §5 Lane map
| Location | Window | Exposure | Surfaces |
|---|---|---|---|
| `loc_bar` | Mon 18:00–20:00 | public | collection (rent intercept) + auto-fire summons `canvas_shark_summons` |
| `loc_shark` | (revealed) | private | `canvas_shark_place` (Boyd) |
L1: 1 (light presence hub on collection night) · L2: 3 (presence/pressure beats as the debt mounts) ·
L3: 0 own (he is the interruptor in *others'* scenes — e.g. walks the floor during a Work shift) ·
capstones: 2.

### §6 Capstones (2)
1. **The summons / Boyd** (A) — `shark_met` *(authored: `canvas_shark_summons` + `canvas_shark_place`)*.
2. **The reckoning** (B) — pay-out vs leverage-out fork; sets the endgame flag.

### §7 Anti-patterns
❌ romanceable Collector. ❌ explicit shouted threats. ❌ comic menace. ❌ him present off
collection-night without a beat reason. ❌ gating a canvas trigger on the engine-set `bar_seized`
(use a canvas-set flag + presence — the build-validator trap). ❌ leverage with no in-fiction stakes.
❌ Boyd and the Collector sounding the same (Boyd = colder accountant).

### §8 Cross-arc
WRITES: `summoned_by_shark`, `shark_met`, the endgame flag (no `awareness` trait — removed; the
debt-enforcer reads player `corruption` + `bar_seized`, it doesn't accumulate its own meter).
READS: `bar_seized` (engine, from missed rent) → unlocks the leverage register; player `corruption`
(hardens the register); `money` / payment history (sharpens or eases him).

### §9 Cross-references
Antagonist / **debt-enforcer** sub-type (`doctrine/03` §7 antagonist; `trait-design.md` — enforcer =
player corruption × economic flag, NOT the witness/awareness model); rent/debt system (`schema/02`
`[settings.rent]`); locked-location unlock contract for `loc_shark` (`doctrine/10` §5.4). Sibling:
**Marcus** (clean-money alternative), **Rosa** (warns). Canvases: the engine rent intercept
(`[settings.rent]`), `canvas_collector_coerce`, `canvas_collector_floorwalk_seized`,
`canvas_shark_summons`, `canvas_shark_place`, `canvas_collision`.

### §10 Acceptance criteria (done when)
- Weekly collection fires via `[settings.rent]` (Mon 18–20), armed only after `debt_explained`.
- Missing payment past grace sets `bar_seized` (`eviction_mode = flag_set` — opens leverage, not game-over).
- Leverage register escalates on player `corruption` × `bar_seized` — **no `awareness` trait** (removed).
- No canvas trigger gates directly on the engine-set `bar_seized` (uses a canvas-set flag + presence —
  the build-validator trap).
- Both endgame routes reachable — pay-out (clean) vs leverage-out — converging on `canvas_collision`.
- Collector never romanceable; Boyd reads colder than the Collector.

---

## Rosa — `npc_rosa` (service — non-escalation)
**scope_mode: full_game.** Ceiling: **non-escalation / support register** (declared explicit but the
arc is non-romance — empty L2/L3 escalation is honest, `doctrine/03` §8.4).

### §1 End-state fantasy
The cook who came with the kitchen becomes the one person in Nina's corner who wants nothing from her.
End-state: the kitchen as safe harbor — Rosa feeds her, covers for her, tells her the truth about
Boyd and about the men circling. A service/ally arc, not a seduction. (If the game later greenlights
a deeper Rosa register, that's a Phase-2+ amendment; in scope she stays support.)

### §2 Voice spec
- **Background:** 50s, runs the kitchen "like a country she founded", apron double-wrapped, points
  with a wooden spoon.
- **Speech patterns:** warm-brusque, imperative, maternal-tough; affection disguised as orders ("Eat
  something before you fall over. Then we talk.").
- **Samples:** R0 "You're Sully's girl. Kitchen's mine. We'll get along." · R1 (trusts) "That man at
  the end of the bar? Don't. I've buried better judgment than yours."
- **Framing:** ally / truth-teller / mother-hen. NO sexual register in scope.
- **BANNED:** Rosa sexualized; Rosa as obstacle; saccharine; filling her empty L2/L3 cells with
  romance/atmosphere texture (the Marge failure mode).

### §3 Ladder (collapsed — 2 tiers, service)
T0 the new owner (`relation 0`) · T1 trusted (`rosa_trusts`, relation 25) — covers for her, real talk.

### §5 Lane map
| Location | Window | Exposure | Surfaces |
|---|---|---|---|
| `loc_kitchen` | 17:00–23:00 | semi-private | Lane 1 hub `canvas_rosa_hub` — talk/advice |
L1: 1 · **L2: 0 · L3: 0 (empty, honest)** · capstones: 1 (the talk where she chooses Nina's side).

### §7 Anti-patterns
❌ sexualizing Rosa. ❌ filling her L2/L3 (empty is honest). ❌ saccharine maternal gloss. ❌ Rosa as
gatekeeper/obstacle. ❌ advice that's never mechanically true. ❌ present outside kitchen hours.
❌ register drift toward romance. ❌ over-long warmth (stay brusque).

### §8 Cross-arc
WRITES: `npc_rosa.relation`, `rosa_trusts`. READS: Marcus/Dee/Collector progress (her warnings
reference whoever's circling) — she is the game's conscience/foreshadow voice.

### §9 Cross-references
Service / non-escalation arc (`doctrine/03` §8.4 — empty L2/L3 is honest); the Marge lessons
(Doc 54 — don't fill service cells with romance/atmosphere texture); relation as the service spine
(`trait-design.md` service = relation). Sibling: she references **Marcus / Dee / Collector** progress
(the conscience voice). Canvases: `canvas_rosa_hub`, `canvas_rosa_trusts`.

### §10 Acceptance criteria (done when)
- The one capstone reachable: `rosa_trusts` at `npc_rosa.relation` ≥ 25.
- L2/L3 deliberately empty — no romance or atmosphere filler.
- Her advice is mechanically true (the men she warns about are real threats in play).
- Never sexualized; stays in `loc_kitchen` on schedule; register brusque-warm, never saccharine.

---

## Dee — `npc_dee` (leverage — transactional escalation)
**scope_mode: full_game.** Ceiling: **explicit** (transactional / credit-for-favors / coercive-lite).

### §1 End-state fantasy
The supplier who sets the credit terms on every bottle — which means he sets how long the bar stays
open. End-state: the terms stop being about money. He extends credit for favors, each one a notch
deeper, until keeping the taps flowing means keeping Dee happy. A transactional escalation she chooses
under pressure. Signature scenes: the first "we can work something out"; the delivery-dock
arrangement; the standing terms.

### §2 Voice spec
- **Background:** mid-40s distributor, clipboard, "a smile that's doing math."
- **Speech patterns:** smooth, breezy, everything framed as a favor he's doing her; the cost arrives
  late in the sentence ("I can float you the order. Course, floating costs me — so it's gotta cost you
  a little too.").
- **Samples:** D0 "New owner! Sully ran a tab. You want the same deal?" · D1 "Terms are flexible for
  the right kind of customer." · D2 "See? Easy. Same time next delivery."
- **Framing:** transactional escalation; affable coercion; never a raised voice.
- **BANNED:** Dee as overt villain; crude early; the favors free of consequence; him romantic/sincere.

### §3 Stat ladder (6 tiers; money/debt + corruption — leverage, NO relation)
The leverage spine is economic, never relation: the terms turn fires when the bar's short AND she's
loosened. T0 on the books · T1 `dee_terms` (flexible terms floated — fires at money < 200 + corruption 10:
short on cash + a little loosened; a flush owner bypasses it) · T2 corruption 25 (first favor at the
dock) · T3 `dee_deal_done` (standing arrangement) · T4 corruption 45 · T5 the taps are his leash.

### §4 Per-rung pretexts (sample)
T1: short on the invoice, he "floats" it. T2: the cellar delivery, door shut. T3: standing terms.
T4/5: escalating dock arrangements.

### §5 Lane map
| Location | Window | Exposure | Surfaces |
|---|---|---|---|
| `loc_wholesaler` | Mon–Fri 10:00–17:00 | public | Lane 1 hub `canvas_dee_hub` — order/terms + locked rungs |
| `loc_cellar` | Tue/Fri 14:00–15:00 | semi-private | delivery hub (higher exposure ceiling) |
L1: 2 · L2: 1 (he's at the dock when she arrives) · L3: 0 · capstones: 3.

### §6 Capstones (3)
1. **Flexible terms** (A) — `dee_terms`. 2. **The dock** (B) — first favor, accept/refuse → `dee_deal_done`.
3. **Standing terms** (A) — `dee_first_done`.

### §7 Anti-patterns
❌ overt-villain Dee. ❌ crude before T4. ❌ favors with no stocking/credit stakes. ❌ raised voice.
❌ him present off delivery/depot hours. ❌ Tier-3 on the repeatable hub. ❌ Dee sincere/romantic.
❌ forgetting the leverage is *the bar's supply line* (mechanical stakes).

### §8 Cross-arc
WRITES: `corruption`, `dee_*` flags; (Phase-2+) bar-stock/credit state. (No `npc_dee.relation` —
the leverage spine is money/debt + corruption; relation was stripped from his arc.)
READS: player `money` (terms turn needs money < 200) + `corruption`; `bar_seized` / debt pressure
(when she's broke, his terms bite harder).

### §9 Cross-references
Leverage sub-type (`trait-design.md` — leverage = money/debt + corruption, never relation);
transactional escalation; capstone + Pattern-F rules (`doctrine/04` §4 — the dock is the Type-B retry).
Sibling: **Collector** (both are economic-pressure antagonists — Dee's leash is the supply line, the
Collector's is the debt). Canvases: `canvas_dee_ropes_first`, `canvas_dee_hub`, `canvas_dee_cellar_hub`,
`canvas_dee_terms`, `canvas_dee_dock`, `canvas_dee_standing`.

### §10 Acceptance criteria (done when)
- All 3 capstones reachable in order: terms → dock → standing.
- Entry (terms) gates `money < 200` + `corruption ≥ 10` (short on cash + a little loosened) — **no relation**.
- Favor at corr 25, standing at corr 45.
- `npc_dee.relation` is written **nowhere** (stripped — the leverage spine is money/corruption).
- The dock is a real accept/refuse fork (refuse re-fires next delivery).
- Leverage always tied to the bar's supply line (mechanical stakes).
- Quest-card corruption goals labelled "My corruption"; hub flat, Tier-3 only in the capstones.

---

## §3 Loose roadmap (seeds the ledger `plan`; fully revisable)
1. First night *(bootstrap — done)* · 2. Sal on-ramp *(npc_intro — done)* · 3. First payment day
*(economic)* · 4. Rosa in the kitchen *(npc_intro)* · 5. Restock — meet Dee *(npc_intro)* ·
6. Marcus, the regular *(npc_intro)* · 7. Dress for tips *(economic/arc)* · 8. Marcus heats up
*(arc_escalation)* · 9. Behind on payment — shark's place unlocks *(location_reveal — done)* ·
10. Sal slow-burn deepens *(arc_escalation)* · 11. Dee's terms *(arc_escalation)* · 12. A collision
*(cross_npc)* · 13. The reckoning *(capstone)* · 14. Endgame *(story_turn)* · 15. Work-the-bar
earning loop *(economic — done)*.
