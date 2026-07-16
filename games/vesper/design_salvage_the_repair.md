# Vesper — Locked Design: Salvage (Act 2, The Repair Bridge)

> ⚠️ **SUPERSEDED (2026-07-16) by `design_salvage_v2.md`.** This is v1 — the tight 2-scene bridge with the
> awakening/build-file verdict and female Kess. It was built + shipped (`b979332`/`a2ec95f`), then reworked:
> the repair became a **repeatable grind**, the reveal became the **chip-as-leash**, and Kess became **male**.
> The cold-open + Kess/berth + debt + the `core_strain`/`core_sealed` mechanic carry forward from here; the
> rest is replaced. **Build from `design_salvage_v2.md`, not this doc.**

> **What this doc is.** The design record for Vesper's next chunk — the short bridge between Bastien's
> captivity and Calloway's Mission 3. It pays the frozen `Core: Failing` promise the captivity chunk left
> in the sidebar, turns the "man who knew her body" hook into play *without* spending Cain, and re-launches
> the sandbox pointed at Calloway → the Site → the chip.
>
> **Provenance.** Direction chosen 2026-07-15 from a 6-angle pitch panel + adversarial canon-cop pass +
> showrunner synthesis (workflow `vesper-next-chunk-pitches`). Engine claims below are grounded in files
> read this session — the `core_strain` band table (`0_systems_spec.toml:137-145`), the release beat
> (`5_scenes.toml:3616-3665`), and the constraints carried from the captivity + underworld-hunt docs.
> Anything not yet verified is marked **⚠️ verify at build**.
>
> **Status:** design **fully LOCKED** — frame, verb, staged beat chain, the meter mechanic, and all six
> decisions resolved with LO on 2026-07-15 (§15). `design_book.md` and `authoring_state.json` are still
> **untouched** — the next step is folding this into `design_book.md` propose-first; this doc is the source
> of truth for the chunk until then.

---

## 1. Context — where this sits

Captivity (0.1.3) ends with Wren on the waterfront at dawn: drain back in its socket, leg carrying her,
and **`Core: Failing` frozen in the sidebar on every screen** — a fault with no cure shipped. She is
holding four words she cannot keep, one of them a name that "fit a lock she didn't know was hers," spoken
by a man who found the drain-seam at the base of her spine *without looking, like a hand going to its own
pocket.* She has no idea who he was.

Two hooks scream off that end-state, and **one chunk answers both:**

1. **The unpaid promise.** `Core: Failing` is the loudest standing debt in the game. The captivity doc
   itself flags it as a nerf-with-no-answer that a later chunk is meant to pay
   (`design_captivity_the_room.md:197,200`). Every screen shows it.
2. **The rescuer mystery.** A man knew her hardware in the dark. That is a thread — and the first one she
   has any reason to pull *for herself.*

Salvage is the move that pays #1 while turning #2 into play, and it does it **without delivering Cain,
naming Vesper, or opening the Site** — all of which stay reserved for the finale. It is a **short bridge
(~8–10 canvases), not a mission.** Calloway (Mission 3) ships *after*, clean, with repair off its back.

> **Decisions locked with LO (2026-07-15):** (1) the meter **visibly flips** `Core: Failing → Core: Locked`;
> (2) the repair is **staged**, and the brought bodies are **weapon-tests** (not just charge-partners); (3)
> the awakening stays **still** — no deliberate first-want, only the involuntary leak; (4) she **walks owing
> a `kess_debt`** that grows per stage (untraceable coin, never company Credits); (5) Reeves' drain-leak
> **names Calloway's file room** now. The prior §15 forks are resolved into the body of this doc.

**Build order this chunk sets up:**
`Salvage` → `Calloway / Mission 3` (domme flip; his drain opens the Site) → `the Site → the chip → the
fracture` (Phase-1 finale). Two optional short interludes (company-notices; solo-want) slot in later once
they have flags to cash.

---

## 2. Frame, and the tests it has to pass

She is too broken to work. She cannot be repaired by the company — a cooked core taken to the company
techs means a **refit, and a refit means a wipe** — and she has just caught something she is not willing to
lose. So for the first time she goes and finds help **off the books, on her own initiative, not on
Mercer's order.**

The three tests every Vesper beat must survive:

1. **Scene, not bar.** The repair is **discrete scenes, count locked** — never a meter you fill by
   repeating. This is the chunk built to *cure* the grind review; it must not exit into one
   (`design_captivity_the_room.md`: "two or three repair sessions, each a scene, not a bar").
2. **Has a verb.** New stance, real agency (§3, §5).
3. **Leaves her changed.** She exits with function restored, the sidebar transformed, a wrong-note she
   can't un-hear, and — for the first time — a reason of her own riding under a company order.

### The verb — the first NON-conquest in the game

| NPC | Verb |
|---|---|
| Renner | seduce-in |
| Marsh | scheme-and-serve |
| Bastien | she is taken |
| Calloway | she runs the register (domme) |
| **Kess (Salvage)** | **supplicant / test-bench — she needs, is worked *on*, her weapons proven on brought bodies** |

She works no target. She is the one who **needs**, who is opened up and serviced — and the bodies the world
brings are not marks to conquer but **live tests for the weapons Kess is rebuilding in her.** It is distinct
from every infiltration verb, and it is separated from captivity's *she-is-taken* by three things:
**consent, repair, and her agency waking back up.** The predator, made prey last chunk, now has to *ask.*
That is the point.

---

## 3. The beat chain — LOCKED

**~8 beats, ~8–10 canvases.** Discrete, mostly linear. Kess repairs in **stages**; each stage fixes a
system, then a **body is brought to TEST whether the weapon/function fires.** Distinct scene per stage,
**count-locked at 2–3, never player-repeatable** — the hard grind-guard (§3a).

1. **The body won't hold.** Waterfront, dawn. Two ordinary loop-attempts — answer Mercer's ping, walk to
   Renner's depot — that **break on input**: the leg buckles on the dock stair, the drain misfires cold,
   `Core: Failing` rides red. She *cannot operate broken.* First un-ordered choice: **don't report it**
   (company techs = the scrap heap; refit = wipe) → go find someone who works hardware off the books. First
   disobedience, unremarked. Sets `salvage_entered`.
2. **Finding Kess / the terms.** New location — Kess's berth (a drained dry-dock off the waterfront). She
   **seeks, does not infiltrate** (predator → supplicant). Kess clocks company steel and moves to throw her
   out (company heat is the one thing a ship-breaker won't touch), then flips **greedy** at the core reading
   — a frame nobody catalogues, **custom / bespoke / hand-built** (NOT "old/decommissioned" — see §11.4).
   Terms: **it is not one fix — it is stage by stage, and each stage costs.** She takes **coin**
   (untraceable), never company Credits (that would tip Vance — the thing Wren is hiding). Wren is short →
   the balance rides out as `kess_debt`.
3. **Stage A — Core & charge. (TIER-3 lives here.)** Kess opens the re-seated drain-seam to work the core.
   The **forensic wrong-note**, flat and certain: *"This wasn't us, wasn't a field medic — somebody who'd
   had their fingers in you before, who didn't need to look."* The repair draws power → she must charge →
   mid-charge, Kess's hands in the seam trip an **involuntary glitch-leak**: old smoke up her own spine,
   half the furious-grieving voice, one **off-page** syllable of the name that fit a lock she still doesn't
   know is hers. She reaches for it and **cannot hold it** — a player action that loses it, not a narrated
   loss. One rationed thought: *"What was that."* **TEST: a body — Tolly (an eager dock runner) — is brought
   to prove she can charge without the core cooking again.** `kess_debt += cost`. Acute fault easing; leg
   steadies.
4. **Stage B — The drain (the clue).** Kess re-checks the drain weapon — the one Bastien stripped and the
   stranger re-seated. **TEST: the drain fires on the anal finish with Reeves — a jittery off-books Vance
   courier — and the drain payload makes him give up that the classified asset build-files live in
   Calloway's file room.** The weapon-test *is* the intel beat (canon: an anal finish is how the drain
   *takes*). `kess_debt += cost`.
5. **Stage C — The emitter (light; may fold into B).** A quick proof the arousal weapon still drops a man.
   Kept only if it earns its own canvas; otherwise folded into Stage B's close or dropped — a bridge stays a
   bridge. `kess_debt += cost`.
6. **The verdict — Core: Locked. (Promise paid.)** Function bought back — leg stable, drain seated true,
   the acute overload bled off. **The sidebar transforms** (§6). But a floor she can't cross: *"The real
   fault's in a partition somebody sealed when they built you. I can't open that. You'd need your own build
   file — and Vance keeps those classified."* **Medical crisis → identity mystery.** She **walks owing the
   `kess_debt` balance** — a recurring off-books creditor, the broke→rich seed lit.
7. **Re-launch → Calloway.** Mercer pings Mission 3: Calloway, the internal Cain-hunt, the classified file.
   For the first time the company's *order* and her own *want* share one address — Calloway's file room
   holds both the record of the hand that saved her and her own build. She accepts; under the order rides a
   reason that is hers. Sandbox re-opens pointed at Calloway → the Site.

### 3a. The grind-guard (load-bearing)
Staged repair is **only** safe as **2–3 distinct scenes** — a different system, a different test, a
different body each — **count-locked and `is_repeatable = false`.** The moment the player can repeat a
repair/test to move a number, it is the exact grind the reviewer flagged, and the chunk re-ships the disease
it was built to cure. Staged-and-distinct = the point; looped = fatal. The debt and the strain relief are
applied **once, on the terminal exit of each staged scene**, never on a re-visitable action.

---

## 4. Kess — the new NPC (casting)

- **Who:** an off-books dockside **synth-mechanic / ship-breaker**, working out of a drained dry-dock at
  the edge of the Reach. She takes apart decommissioned machines for parts and does quiet, illegal repair
  on the side.
- **First voiced line = her want (the casting hook):** money, and the interesting problem. She reads
  **bodies as hardware, not women** — Wren is a *frame*, a *build*, a puzzle nobody's supposed to be able
  to afford. That clinical eye is exactly what makes her the mystery's second channel: she reports what she
  *sees in the metal* without knowing, or caring, what it means about who touched Wren before.
- **Role, doubled:** she is **the hand that repairs her AND the eye that reads who knew her** — the fusion
  character. She never learns Cain's name, never reports an alliance, never notices "her readings drift"
  (that last is **Pell's reserved door** — keep Kess off it, §11.5).
- **Shape:** full NPC — portrait, berth location, slug `kess`. **Not** a conquest target (no
  relation/corruption climb). **She recurs into Act 2** as a debt-holding off-books contact (LO-locked) —
  the `kess_debt` balance is the live thread.
- **Tolly + Reeves:** *not* full NPCs. Narration-level **test-bodies**, named in narration only,
  canvas-local — the same treatment as the captivity crew (no `npc_` objects). Their job is to be the live
  test each repaired system is proven on: Tolly = the charge/core test (Stage A), Reeves = the drain test
  whose payload drops the Calloway clue (Stage B).

---

## 5. The room and the stance

### 5.1 Kess's berth
One new location, `kess_berth` (working name), attached `entry_from = the_waterfront` so its exit link is
free and ungated (the same nav mechanism the captivity doc verified, `design_captivity_the_room.md:§9.1-9.2`)
and so it sits exactly where captivity dumps her. Ordinary location — no seal, no captivity machinery.

### 5.2 The supplicant stance
The interaction is inverted from every other arc. She is **not** working a mark up a ladder; she is the one
being **worked on.** Agency lives in: the choice to seek help vs report (beat 1), the terms she takes
(beat 2), reaching for the fragment inside the leak (Stage A), and clicking through each staged
repair-and-test. None of it is a bar. **If the player can spam an action here to raise a number, it is the
wrong action.**

---

## 6. The meter — `Core: Failing` → `Core: Locked` (engine-true)

**The corrected mechanic** (the pitch panel's "add a band below 72" is wrong — 1–71 is fully occupied;
see the verified table in §11.1). Two moving parts, both additive, both extend-only:

1. **The acute overload is relievable.** `core_strain` *is* the acute overload number. Kess can honestly
   **bleed it toward 0.** At 0 the "Core: Failing" row **vanishes** — the renderer emits nothing when no
   band matches, exactly what `0_systems_spec.toml:128-130` says happens "if the fault were ever cured."
   This is not a cheat; the number was always the acute pressure, and Kess relieves it.
2. **The permanent fault gets its own row.** A **new hidden trait `core_sealed` (0 → 1 on repair)** drives
   a **new `trait_status_text` sidebar row: "Core: Locked."** It appears only when `core_sealed >= 1`. This
   is the sealed partition — the true fault Kess *cannot* open. Only the Site / the build file opens it.

Net player experience: the red **Failing** row they've watched frozen since captivity **finally changes** —
crisis resolved — and a steady **Locked** row rides on in its place as the standing promise the finale
pays. Honest to `design_captivity_the_room.md:197` ("no cure shipped" — the true fault is uncured, only
Locked) *and* it pays the sidebar promise loud.

**⚠️ verify at build:** (a) nothing else gates on `core_strain` in a way that misfires when it hits 0 (the
captivity use-scenes are consumed one-shots behind `captivity_done`, but confirm live); (b) old-save cohort
— a player who already finished captivity has `core_strain=96` and no `core_sealed`; the Failing row keeps
rendering for them until they play Salvage, which is correct.

**LOCKED (LO): the meter visibly flips.** The `Core: Failing` row the player has watched frozen since
captivity clears, and `Core: Locked` takes its place — the player gets the visible payoff for finishing the
chunk. (Not the frozen/narrative-only alternative.)

---

## 7. The mystery — what it spends, what it saves

Two touches, both **cold-channel** — they move the Cain thread forward without him on the page:

- **The forensic read (Stage A).** Kess, reading metal: *someone who'd had their fingers in you before, who
  didn't need to look.* This confirms the cell's rescuer through hardware evidence. It attributes the
  **tender** hand to the **recent re-seat** — canon-correct: Bastien's crew stripped the drain violently at
  the *start* of captivity; Cain re-seated it expertly at the *release* (`5_scenes.toml:3640-3641`). Kess
  names **no one.**
- **The glitch-leak (Stage A, Tier-3).** An involuntary memory surfacing, **reusing the release beat's exact
  protected devices** — the smoke, the hand straight to the seam, the name that fits a lock — so it reads as
  *the same memory*, not a new fact. The **syllable of the name never renders as printed text** and is **NOT
  a chip fragment** (the Site owns the first fragment). Dread-first: her body reaches before her mind can
  name it; she is the last to know.

**Spent: nothing reserved.** Cain stays a shape (no `npc_cain`, no voice, no face). "Vesper" stays off-page.
The Bastien–Cain alliance stays unreportable — **Kess doesn't know it.** The Site stays closed.

---

## 8. The awakening — kept still (LOCKED)

The break, plus the name that fit a lock, cracks the still-point open a hair — but Salvage does **not** feed
it. **LOCKED (LO): she stays still.** Her only stir is the **involuntary** memory-leak in Stage A, which she
cannot control and cannot hold. **No deliberate first-want** — the first time she *chooses* to want is saved
for a dedicated later beat, protecting the ledger's "un-fed until the chip" inversion
(`authoring_state.json:109-122`).

**No solo-sexual ladder, no visible "Awakening" meter this chunk.** The want lives only in the leak, rationed
to the flat still-point voice she has had all game (one `thought_bubble` per scene, per the captivity
discipline). The body-test scenes (Tolly/Reeves) are functional and hot but carry **no** "she wanted it"
beat — the horror/pathos is that she is being *operated*, and only the leak reaches past it.

---

## 9. What she carries out

- **Function restored.** Leg stable, drain seated true, the acute crisis over.
- **The sidebar transformed** — `Core: Locked` as the new standing promise (the visible flip).
- **A wrong-note she can't un-hear** — someone knew her body, and she caught a syllable of a name.
- **A destination that is now doubly hers** — Calloway's file room holds both the record she wants and the
  build file she needs. Mercer's order and her own reason point at the same door.
- **A growing debt to Kess** (`kess_debt`, in untraceable coin) — she walks out **owing** it; a live hook a
  later chunk cashes, and the first spark of the broke→rich economy seed. Kess becomes a recurring contact.

She walks back into the same sandbox — Mercer, Renner, the Sunday brothel — repaired enough to work, with
a mystery that is now *hers* and a mission that finally serves it.

---

## 10. Register

Per the `author-game` skill, not this doc:

- **Kess's berth, the terms, the two body-scenes (Tolly/Reeves)** → **RTS-flat.** Terse, specific, crude,
  re-readable, real anatomical language. Kess's own voice is **clinical** — she narrates a body the way a
  mechanic narrates an engine. The bodies are consensual and hot; no ceiling on explicitness.
- **The glitch-leak in session one** → **Tier-3, earned, once-only.** The single place the prose spends —
  and it spends by *reusing* the release beat's devices, so the spend reads as recurrence, not new purple.
- Everything else stays flat. **Specificity, not literary density.**

---

## 11. Engine findings & constraints

### 11.1 The `core_strain` band table — VERIFIED (`0_systems_spec.toml:137-145`)
```
min 1–23   → Core: Nominal
min 24–47  → Core: Hot
min 48–71  → Core: Faulting
min 72     → Core: Failing   (NO max — an unset max defaults to 1e9, so the frozen 96 still matches)
```
1–71 is fully occupied. There is **no free band below 72** to "drop into" — hence the §6 mechanic (relieve
`core_strain` to 0 + a new `core_sealed` row) rather than a new low band.

### 11.2 Gates on TRAITS, not flags — VERIFIED pattern
Any new state the chunk gates content on (repair progress, want-state, the glitch) must be a **hidden
trait**, not a flag, if its setter is triggerless — or the flag-chain validator hard-fails the build
("MISSING HINT"). This is why captivity/underworld used `drains_done`, `names_known`, `core_strain` as
traits. `core_sealed` follows suit.

### 11.3 `version = "1.0"` on every new conditions block — VERIFIED
A conditions block missing it **fails open** (returns true), so new gates would show from game start. Every
new block in this chunk carries it.

### 11.4 The build-fiction correction
Kess reads the frame as **custom / bespoke / hand-built / nobody's-catalogue** — **never
"old / decommissioned."** Wren is a *live prototype*; "old" contradicts canon. This is a load-bearing word
choice, not flavor.

### 11.5 Reserved doors to keep Kess OFF
Kess reads a **body** and points at a **file.** She does **not** notice "her readings drift over time" —
that drift-arc is **Pell's reserved door** (a later company-notices beat). Keep the two clean.

### 11.6 The debt currency — RESOLVED (`1_metadata_and_locations.toml:28-43`)
Two currencies exist: `money`/"Credits" (company money, up-top, traceable) and `coin` (untraceable
underworld scrip, "her own money the company can't see"). Kess — an off-books ship-breaker dodging company
heat — takes **coin, never Credits** (Credits would tip Vance, the exact thing Wren is hiding). Wren is
short, so **`kess_debt` (a new trait) accrues the unpaid balance per stage** and she walks out owing it.
⚠️ Still confirm at build whether a Reach-edge berth reads `coin` as spendable there (coin is normally
underworld-gated); if not, `kess_debt` alone carries the fiction — she never pays, only owes.

### 11.7 ⚠️ Verify at build
- **Nothing else reads `core_strain` at 0** in a way that misfires (§6).
- **`core_sealed` + `kess_debt` sidebar rows render** with the same `trait_status_text` shape captivity used
  (bands from `min = 1`, absent at 0).

---

## 12. Save-safety

Vesper is **shipped — extend only.** No renaming existing ids, flags, traits, stat scales, or the title.

- **New only:** `kess` (NPC slug), `kess_berth` (location), `core_sealed` + `kess_debt` (hidden traits),
  one new `trait_status_text` row ("Core: Locked"), `salvage_entered` + per-stage progress flags, and the
  Salvage canvases. Nothing existing is renamed. **No new "want" trait** — the awakening stays still (§8).
- **Old-save cohort.** A player who finished captivity is standing on the waterfront with `core_strain=96`,
  `captivity_done` set, no `core_sealed`. Salvage's entry gate = `captivity_done is_true` (+
  `salvage_entered is_false`), so the bridge opens for exactly them. The Failing row keeps rendering until
  they play it. New players reach it the same way after captivity.
- NPC state survives rebuilds (stable slug ids; no-DB default). Player traits/flags backfill.
- **Reset the shared sex-loop traits** (`sex_stage`, `loop_npc_pleasure`, `sex_finisher_type`,
  `anal_active`, `sex_entry_origin`) on entry and exit of each Salvage sex scene, per the captivity
  precedent, or state bleeds into Marsh/Renner loops.

---

## 13. Build sequence (propose-first; one verified piece per turn)

Source phases → `merge_toml_phases.py` → `package_from_toml`. **Never hand-edit `7_final_game.toml`.**

1. **Systems:** declare `core_sealed` + `kess_debt` in `0_systems_spec.toml`; add the "Core: Locked"
   `trait_status_text` row (bands from `min = 1`); hide the traits from the dump.
2. **Geography:** `kess_berth` (`entry_from = the_waterfront`) in `1_metadata_and_locations.toml`; init the
   new traits/flags.
3. **Kess:** NPC entry (portrait, berth, the casting hook line) + her intro/terms canvas.
4. **Beat 1:** the two loop-attempts that break on input + the don't-report fork (auto-fire on
   `captivity_done is_true` + `salvage_entered is_false`; sets `salvage_entered`).
5. **Stage A (Tier-3):** the seam + the forensic read + the glitch-leak + the charge, tested on Tolly;
   relieve `core_strain` across the stages (or at the verdict); `kess_debt += cost` on the terminal exit.
6. **Stage B:** the drain re-check + the drain-test on Reeves whose payload drops the Calloway file-room
   clue; `kess_debt += cost`. **Stage C (emitter)** only if it earns a canvas, else folded/dropped.
7. **The verdict:** `core_strain` → 0, `core_sealed = 1`, sidebar flips to "Core: Locked", the "you need
   your build file" line; she **walks owing** the `kess_debt` balance.
8. **Re-launch:** Mercer's ping → Calloway dispatch; sandbox re-opens.
9. **Merge → green build → live-test both cohorts → clean rebuild** (no `--dev --debug`).

---

## 14. Verification plan

Green build: new gates are traits (not triggerless flags); every new conditions block carries
`version = "1.0"`.

Headless SugarCube harness:
1. **Entry gate.** `captivity_done` cohort reaches beat 1 on the waterfront; pre-captivity saves do not.
2. **No grind.** Assert each repair scene is a one-shot (`is_repeatable = false`); assert there is no
   action the player can spam to move a number.
3. **The meter flips.** Before: "Core: Failing" renders (`core_strain=96`). After the verdict: `core_strain`
   → 0 → Failing row **absent**; `core_sealed=1` → "Core: Locked" row **present**.
4. **The debt accrues.** `kess_debt` increments once per staged scene (terminal exit only, never
   re-triggerable); she exits owing the balance.
5. **The leak.** Stage A fires the glitch-leak once; the syllable never renders as printed text; it sets
   no chip-fragment.
5. **Re-launch.** After the verdict, Mercer's Calloway dispatch is reachable; the sandbox loops (Renner,
   the House) still work.
6. **Old-save cohort.** Sim a finished-captivity save → Salvage opens → verdict → meter flips → Calloway
   dispatch.
7. **Zero JS errors** throughout.

---

## 15. Decisions — LOCKED with LO (2026-07-15)

1. **The core payoff → VISIBLE FLIP.** `core_strain` → 0 (Failing vanishes) + the new "Core: Locked" row.
   The player sees the reward for finishing the chunk. (Not frozen/narrative-only.)
2. **Breadth → BODIES AS WEAPON-TESTS, STAGED.** Kess repairs in stages; each stage's brought body is the
   live test the repaired weapon/function is proven on (Tolly = charge/core, Reeves = drain). Count-locked
   2–3, never player-repeatable (§3a).
3. **The fixer → RECURRING.** Kess carries a flicker of greed and holds the debt — a live wire into Act 2.
4. **The debt → WALK OWING IT.** `kess_debt` accrues per stage in untraceable coin; she exits owing the
   balance. Lights the broke→rich economy seed (§11.6).
5. **The awakening → KEPT STILL.** No deliberate first-want; her only stir is the involuntary Stage-A leak
   (§8). The true first *chosen* want is saved for a later beat.
6. **The Calloway crumb → PLANT IT NOW.** Reeves' drain-payload names Calloway's file room; her private want
   and Mercer's Mission-3 order fuse at one address.

---

## 16. Explicitly deferred (not this chunk)

- **Calloway / Mission 3** — the domme power-flip; his drain opens the Site. Built clean *after* Salvage.
- **The Site → the chip → the fracture** — the Phase-1 finale; the first chip fragment; the sealed
  partition Kess named but couldn't cross.
- **The company-notices chunk** (Pell/Vega; the wipe threat with teeth) — once its flags have downstream to
  cash.
- **The solo-want interlude** — the first *deliberate* want, saved out of this chunk (Salvage holds her still).
- **Bastien's alignment with Cain** — still the saved bombshell.
- Cain on-screen / the name "Vesper" / warmth — reserved.

---

## 17. Skill note

The `author-game` skill has **no doctrine for a non-conquest verb** — a stance where the player is the one
worked *on*, needing rather than taking. Its lane model assumes a protagonist who chooses a target and
climbs. Salvage's *supplicant* stance is designed here from first principles, the same way captivity's
agency-less *attention* verb was. If it works, "the roster needs a verb where she needs, not takes" belongs
in the skill — or the next author writes every repair/aftercare beat as a passive cutscene.

---

## 18. Step-6 feedback — gaps closed (2026-07-15)

A 4-lens Step-6 audit (grind · voice · world/NPC · machine/save-safety) graded this chunk **FIX_THEN_GO** and
surfaced 10 gaps. All resolved here before authoring; the load-bearing mechanics are also carried into the
`design_book.md` blueprint.

### MAJOR

**G1 — The inter-stage DAG is pinned (was a buildability blocker).** `is_repeatable = false` blocks re-runs
but does NOT sequence distinct canvases — on `salvage_entered` alone the router could fire the verdict before
the tests, collapsing the staged structure. Explicit gates (every block `version = "1.0"`):
- **Beat 1** (body won't hold): auto-fire @`the_waterfront`, **high priority**, `captivity_done is_true` +
  `salvage_entered is_false`.
- **Stage A**: `salvage_entered is_true` + `salvage_stage_a_done is_false`.
- **Stage B**: `salvage_stage_a_done is_true` + `salvage_stage_b_done is_false`.
- **Verdict**: `salvage_stage_b_done is_true` + `salvage_done is_false`.

Each stage sets its `_done` flag on its **terminal exit**; the chain is a strict DAG, cold-start-reachable
from `captivity_done`.

**G2 — Voice carriage is pinned; present bodies SPEAK (fixes the skill's #1 defect).** The captivity
crew-narration exemption does **not** transfer — it rode on dissociative object-state, and §8 confirms that
state is gone (she's present, conscious, clinical). Per-beat carriage:
- **PLAYED** (target ≤ 1.5:1 narration:dialogue; > 3:1 FAILS): **beat 2 terms · Stage A (Kess's reads) ·
  Stage B · the verdict.** Kess's clinical reads **are her lines** — write "Kess says what she sees," never
  "she narrates a body." **Reeves' drain drops him and HE says where the files are** (the Calloway hand-off
  is a spoken line, not narrated summary). **Tolly = one terse eager line.** Test-bodies render
  `speaker = "unknown"` → a played **"Stranger:"** line (v2.py:14097) — no `npc_` object needed.
- **NARRATED (legitimate exemption):** the Stage-A leak (interior, no holdable speaker) · beat 1 (solo) ·
  the interior end-cards.

**G3 — The berth's post-chunk lifecycle is resolved: CLOSE-after (no dead room).**
`entry_from = the_waterfront` makes `kess_berth` a permanent ungated venue; captivity's sealed-root precedent
does NOT apply (opposite topology). Resolution:
`kess_berth entry_conditions = { salvage_entered is_true AND salvage_done is_false }` (`version = "1.0"`) +
a `blocked_message` that telegraphs the dormant seed (e.g. *"Shuttered. Kess doesn't work twice on the same
debt — not until she calls."*). Enterable during the repair, **locked-visible after.** The verdict teleports
her back to `the_waterfront`. **Kess is chunk-scripted only — NO schedule** (so she never leaks onto the
Schedule page; npc-intro step 7). Recurrence is deferred to the chunk that re-opens the berth.

### NOTABLE

**G4 — The debt has a named address.** `kess_debt` is not a floating accumulator: the reserved downstream is
**Kess comes to collect** (or claims first refusal on the custom frame) in the Act-2 chunk that re-opens the
berth — the debt gates a later off-books repair / forces the first coin-earning choice that lights the
broke→rich economy. Her Act-2 pull-reason = the coin she's owed. (A deferred seed *with an owner.*)

**G5 — Coin NEVER blocks (hard rule; closes the §11.6 warning).** Stage progression gates ONLY on the
`salvage_stage_*` flags — **never on a coin balance the player must earn.** Each stage's cost ALWAYS accrues
as `kess_debt` and never blocks a broke player. No build may wire a payment/`costs` gate on the stages. This
kills the return-to-earn grind loop the bridge exists to avoid.

**G6 — The sandbox stays SOFT-OPEN; beat 1 is self-contained.** The bridge does **not** retro-gate the
shipped Renner/Mercer/House loops (that would violate extend-only). The "she cannot operate broken" fiction
is held **beat-1-local**: beat 1 is ONE self-contained auto-fire canvas that **narrates** both failed
loop-attempts (it does not intercept or edit the live Mercer/Renner canvases). Beat 1 is **single-exit**
(forced don't-report) — no dangling "report" branch to soft-lock.

**G7 — Mission-3 re-launch is wired, not just narrated.** Beat 7 adds a **`mission_3_active` flag** flipped
at the verdict (alongside `salvage_done`) + a **Tier-1 Story Goal quest card** gated `salvage_done` (mirrors
Mission-1's card, `5_scenes:1479-1482`). NOT Calloway's arc — only the card + flag + the Mercer dispatch.

### MINOR

**G8 — No in-scene farmable meter.** (Added to §3a.) No in-scene meter (arousal / exposure / sex-loop
pleasure) is farmable — the sex-loop trait reset on entry/exit is the guard; nothing the pose menu touches
persists or accrues.

**G9 — Register wall around the reused leak.** Reuse `beat_0042`'s emotional **devices** (old smoke · the
hand straight to the seam · the name that fits a lock) but NOT its periodic cadence or its **Rule-5-BANNED**
impersonal-"you" analogies (*"the way you'd say the price of a thing"*, *"like a hand going to its own
pocket"*). Strip the simile from any reused fragment. **Kess's reads are terse spoken clinical lines — never
a narrator "the way you'd…" inference.**

**G10 — Declared-leans + verifications recorded.** (1) The bridge's single-thread window is a **declared §2F
lean** (a directed chunk, thin ON PURPOSE — not an accidental thin day). (2) **Meter-flip verified safe:**
every `core_strain` reader is co-gated `captivity_broken is_false` / `@captive_room` — all dead post-release,
so relieving it to 0 misfires nothing. (3) The **consensual / clinical / no-degradation / no-"she-wanted-it"
ceiling** carries verbatim into the blueprint berth notes. (4) Beat 1's don't-report choice plants a **Kess
pointer** ("a ship-breaker in the Reach who works off the books"); she renders `speaker="unknown"` →
"Stranger:" until she names herself.
