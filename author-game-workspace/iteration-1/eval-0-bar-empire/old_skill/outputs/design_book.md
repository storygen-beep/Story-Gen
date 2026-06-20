# Bar Empire — Design Book

*The intent record. Stable; amend explicitly (bump `book_revision` in the ledger).*

## World setup

**Premise.** A female PC, broke and behind on her own debts, waits tables at **The Velvet Spur** —
a sleazy strip-adjacent dive bar owned by a man who treats the floor, the till, and the women on it
as his personal property. The fantasy is a three-act inversion of that ownership:

1. **Seduce and corrupt the owner** — turn his appetite into a leash, until he signs the bar over.
2. **Take the bar out from under him** — the leverage capstone; the deed changes hands.
3. **Build an empire** — recruit and corrupt other women into your stable until you are the madam
   the city answers to.

This slice authors **Act 1** to a gold standard (the Marco seduction-and-leverage arc) plus the
minimum-contract on-ramps for the women who become the Act-3 stable. Acts 2/3 are telegraphed via
locked-visible rungs and seeded plan rows; they are not authored in the slice.

**Player.** Dahlia, 26. Customizable name (`@player`) + build + look — emitted as `@`-tokens so the
rename propagates (`doctrine/14`). Night-centric orbit: she sleeps days, works the bar nights.

**Economic engine.** Money pressure is the spine: she owes the bar a running tab/debt that Marco
holds over her (the leverage hook — her debt is HIS instrument before she turns it into hers). She
earns by working shifts (a solo Lane-3 work host that also carries the job-lewd feeder ladder).
**Energy** is the paced resource: a shift COSTS energy (gated via `costs`, never `effects`), restored
by the day-advance **Sleep** activity.

**Time model.** Continuous clock, day-cycle phases (a label convention over the clock):
Morning (06–12) / Afternoon (12–17) / Evening (17–21) / Night (21–03) / Asleep. Night-centric: the
bar lights up Evening→Night. The **Sleep activity is the day-cycle router** (`doctrine/04` §10):
she sleeps the day window, which carries her across the clock so the daytime errand/clothing window
is reachable — without it daytime content is dead (the Dee-bug).

**`scope_mode`: `slice`.** ~10–14 day validating chunk: **1 gold NPC (Marco)** at full depth + 3 at
minimum-contract + locked-visible rungs telegraphing the deferred empire. **All four Phase 2+
decisions DEFER — no Q&A** (pregnancy / scandal / gallery / tracker all deferred per slice rule).

**Optional systems.** **Clothing = ON** (`[settings]`) — the bar is a public/exhibitionism surface;
clothing gates PUBLIC floor content + feeds the exhibitionism odometer (it NEVER gates an NPC arc).
Rent-as-system and phone = OFF in the slice (debt is modeled as a `money`/flag pressure, not the rent
engine, to keep the slice minimal).

**Loose roadmap (a hypothesis, reorderable — seeds the ledger `plan`):**
1. Intro: broke morning, walk to the Spur (boot canvas — *setup*).
2. Get hired / put back on the floor by Marco → Marco Lane-1 hub. *(beat 1 — the continue beat run here)*
3. Meet Jolene (fellow waitress) — on-ramp.
4. Meet Reggie (a regular) — on-ramp.
5. Open the back room (locked) — the private surface Marco's arc escalates into.
6. Marco escalation rungs (tease → contact → after-close).
7. Job-lewd feeder ladder on the work shift (corr 0 → 15 → 30 floor).
8. Marco leverage capstone — the deed changes hands (Act-1 terminal).
9. *(Act 3, deferred)* recruit Jolene + Sasha into the stable.

## Locations (the graph)

- `loc_dahlias_room` — her cheap rented room (home hub; Sleep + clothing wardrobe live here). Reachable.
- `loc_rooming_house_hall` — pass-through corridor to the street. Reachable.
- `loc_city_street` — the town hub; the Spur, a thrift store, the day errand surface hang off it. Reachable.
- `loc_spur_floor` — The Velvet Spur main floor (the night hub; Marco + Jolene + Reggie). Reachable.
- `loc_spur_backroom` — the owner's private back room. **Locked** (`marco_backroom_access`);
  unlock contract Case B — opened by the Marco "after-close" beat, off-hours fallback otherwise.
- `loc_spur_office` — Marco's office (the deed lives here; the leverage capstone surface).
  **Locked** (`marco_office_access`).
- `loc_thrift_store` — second-hand clothes (the clothing shop; daytime errand). Reachable.
- `loc_marco_home` — Marco's place across town. **Offscreen** (`offscreen = true`) — his daytime
  away-block, non-navigable, exempt from the presence floor.

## Per-NPC R7 briefs

### Marco — GOLD STANDARD (slow-burn seduction → leverage). Ceiling: explicit (max).

1. **End-state fantasy.** Marco starts as the owner who looks at Dahlia the way he looks at the till
   — an asset he's already counted. The arc ends with that ownership reversed: he has signed the
   Spur over because his wanting her became the one debt he couldn't carry. The destination is the
   deed in her hand and him still showing up, leashed, because she lets him.
2. **Voice spec.** Proprietary, transactional, never tender at Lane 1/2/3 — RTS-flat, ~30 words,
   crude at his ceiling. He talks about her like inventory until the leash flips; the *register*
   stays flat-and-specific even as the power inverts. Tier-3 spend reserved for capstones only.
3. **Stat ladder + gating spine.** Seduction arc → **spine = player `corruption` odometer** (the
   depravity she's willing to trade) **+ Marco `arousal` throttle** (his appetite, resets at climax,
   drives the repeatable loop) **+ the leverage flag chain** (`money`/debt + `marco_*` flags). NOT
   `relation`-on-everything. Rungs gate on the corruption odometer; the leverage CAPSTONE gates on
   the odometer + flag chain, NEVER on arousal.
   - Stage 0 Counting-her (corr 0, baseline) → 1 Noticed `marco_noticed` (corr 5) → 2 Tease/contact
     `marco_contact` (corr 15) → 3 After-close `marco_backroom_done` (corr 25, opens backroom) →
     4 His-arrangement `marco_arrangement` (corr 35) → 5 Leash-flips `marco_signed` (corr 45 + debt
     cleared + office access — the deed).
   - Vocab ceiling: explicit (default-to-maximum, `doctrine/08`).
4. **Per-rung pretext shapes.** Pour-his-whiskey (talk) → lean-across-the-bar (tease) → let-him-walk-
   you-to-the-backroom (contact) → after-close-alone (backroom) → the-arrangement (office/leverage).
5. **Lane-by-lane map (slice = ~40% of full budget).** L1: Spur-floor hub (pour/talk/tease/blow-off)
   + backroom hub once unlocked. L2: 1 ambient (he watches you across the floor). L3: the work-shift
   walk-in (he corners you mid-restock). Capstones: after-close (Type A) + the deed-signing (Type B
   leverage terminal).
6. **Capstones.** `scene_marco_after_close` (Type A; gate corr 25 + `marco_contact`; sets
   `marco_backroom_done`, opens `loc_spur_backroom`). `scene_marco_signs_over` (Type B leverage
   terminal; gate corr 45 + debt cleared + `marco_arrangement`; sets `marco_signed`, opens
   `loc_spur_office`). Both gate on the **odometer + flags**, never arousal.
7. **Anti-patterns.** Don't gate his entry on anything she can only earn inside his arc (no backwards
   on-ramp). Don't make `relation` the spine. Don't surface his arousal as a tender meter.
8. **Cross-arc writes/reads.** Sets `marco_signed` (Act-3 stable recruiting reads it — you own the
   venue the women come to). Reads the `debt_cleared` economic flag.
9–10. **Cross-refs + acceptance.** Done = corr-45 leverage capstone reachable through ordinary
   shift-and-seduce play; deed changes hands; backroom + office unlocked legibly.

### Jolene — fellow waitress (service → future stable recruit). Ceiling: explicit. MINIMUM-CONTRACT.

1. **End-state.** The first woman you bring into the stable once you own the bar (Act 3, deferred).
   In the slice: a warm-conspiratorial floor colleague who teaches you the till and the regulars.
2. **Voice.** RTS-flat, wry, tired-warm. 3. **Spine = `relation`** (service shape; light — no own
   corruption odometer, no arousal throttle; that gold model is Marco-only, `rts P5`).
   4–7. Slice: one Lane-1 floor hub + a locked-visible "bring her in" rung (Act-3 telegraph).
   8. Reads `marco_signed` for the deferred recruit beat. 9–10. Done = meetable cold, recruit rung
   visible-but-locked.

### Reggie — a regular (peer). Ceiling: explicit. MINIMUM-CONTRACT.

1. **End-state.** A paying regular who becomes a customer of the empire (deferred). Slice: ambient
   regular at the bar, a face who tips and talks. 2. RTS-flat, blustery. 3. **Spine = `relation`**
   (peer; light, no Lane 3). 4–7. One floor hub. 8. none in slice. 9–10. Done = meetable cold.

### Sasha — a dancer (light; future stable). Ceiling: explicit. MINIMUM-CONTRACT / TELEGRAPH ONLY.

Named in the roster + plan as the second Act-3 recruit; **no canvases in the slice** — a locked-
visible "recruit Sasha" rung telegraphs her. Spine = player corruption (recruiting) when authored.

## Content roster

*Two tracks. NPC-arc track (Marco gold + 3 light) AND the player/world lewd feeder catalog that
feeds the player corruption/exhibitionism odometers (the supply Marco's floors demand). Slice =
thin-but-tier-complete feeder spine + Marco's full Act-1 arc.*

| venue / host | title | track | arch | lane | tier | fire | hook | gate |
|---|---|---|---|---|---|---|---|---|
| `loc_spur_floor` | Marco floor hub | NPC:marco | 6/bridge | 1 | corr 0→45 | deterministic | the owner who counts you | presence |
| `loc_spur_floor` | He watches you | NPC:marco | 7 | 2 | corr 15 | random 25% | caught his eye mid-shift | `marco_noticed` |
| `activity_work_shift` | He corners you | NPC:marco | 6 | 3 | corr 15 | random 30% | walk-in mid-restock | `marco_contact` |
| `loc_spur_backroom` | After close | NPC:marco | — | 4 | corr 25 | deterministic | the night he locked up | `marco_contact` |
| `loc_spur_office` | He signs it over | NPC:marco | — | 4 | corr 45 | deterministic | the leash flips | `marco_arrangement`+debt |
| `loc_spur_floor` | Jolene floor hub | NPC:jolene | — | 1 | relation | deterministic | she runs the till | presence |
| `loc_spur_floor` | Reggie regular hub | NPC:reggie | — | 1 | relation | deterministic | the regular who tips | presence |
| **PLAYER FEEDER TRACK (the supply)** |
| `loc_dahlias_room` | Touch yourself | solo | 1 | solo | **corr 0** | deterministic | bootstrap off zero | none (ungated) |
| `activity_work_shift` | Work the floor in less | solo | 4 | solo | corr 15 + exb 10 | deterministic | job-lewd: serve in a thong | revealing outfit |
| `loc_spur_floor` | Flash a regular | solo | 2 | solo | corr 15 + exb 10 | deterministic | a flash for a bigger tip | exb 10 |
| `activity_work_shift` | The VIP table | solo | 4 | solo | corr 30 | locked-visible | the corr-30 job-lewd floor | corr 30 |

**Feeder economy balance.** Marco's seduction floors sit at corr 5 / 15 / 25 / 45. The feeder
supply: corr-0 solo bootstrap (gets her off zero) → corr-15 flash + job-lewd-in-less (the mid-game
workhorse, two venues) → corr-30 VIP locked-visible. The supply tiers under each Marco floor, so the
floors are reachable through ordinary shift-and-flash play (not starved — the Last Call lesson).
Slice ships ≥1 bootstrap + ≥1 flash per active venue; the corr-30+ rungs are locked-visible
telegraphs.
