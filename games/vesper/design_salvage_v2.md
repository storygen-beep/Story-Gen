# Vesper — Locked Design: SALVAGE v2 (the repair grind + the leash)

> **What this doc is.** The design record for the **reworked** SALVAGE chunk. It **supersedes**
> `design_salvage_the_repair.md` (v1 — the tight 2-scene bridge with the awakening/build-file reveal, already
> built + shipped to the portal as `b979332`/`a2ec95f`). v2 keeps v1's cold-open, Kess/berth, debt, and the
> `core_strain`/`core_sealed` mechanic, and **replaces** the middle and the ending: the repair becomes a
> **repeatable grind loop** where her power returns across sessions, and the ending is the **chip-as-leash**
> reveal instead of a build-file. Kess is now **male**.
>
> **Status:** ✅ **BUILT + live-verified 2026-07-16** — green build (flag chains valid) + headless test of the
> full spine: hub → pay 20 coin → arm → band scene → `core_strain -8`; band routing; chip-snag @ Hot; verdict
> @ session 12 → chip-as-leash reveal → `core_sealed=1` lights **Leash: Uncut** + bands clear → teleport →
> `salvage_relaunch` (Mercer wary + Calloway); Mercer shocked @ penthouse mid-repair. Zero page errors.
> **NOT yet committed/pushed** — awaiting LO's deploy go. Media (~30 assets) deferred to the 0.1.4 pass. All
> dials resolved (§18); one reversal from the first lock — coin-cost-per-session, not debt-accrual (§3, §10).
> `design_book.md` + `authoring_state.json` to be updated on the deploy go.
>
> **Provenance.** Reworked with LO 2026-07-16 across a design conversation. Engine claims reuse the verified
> captivity model (`design_captivity_the_room.md` §9; the `core_strain` band renderer, the band-gated shelf
> scenes) and the v1 SALVAGE build. Anything not yet verified is **⚠️ verify at build**.

---

## 1. Context — what changed from v1, and why

v1 shipped as a tight bridge: 2 count-locked repair scenes, then a verdict that revealed a "sealed partition"
needing her **build file**, which a drained courier (Reeves) conveniently located in **Calloway's file room**
— fusing her personal repair to Mercer's Mission-3 with a bow. LO's calls in the rework:

1. **Kess should know nothing about the company/missions.** He reads *hardware*, reports about *Wren*. So the
   Calloway/build-file clue is **cut** from Kess and Reeves entirely.
2. **The repair should be a GRIND** — a repeatable job she works at across days, her power returning session by
   session — **not** an instant 2-scene fix. (Grind is fine; *content-free* grind is the disease. This grind
   delivers a scene every time — the RTS model, not the mopoga one. See §3.)
3. **The "chip" is a control LEASH, not an awakening or a build-file.** It's *why she can never turn her power
   on Mercer.* Kess can't pull it — that needs its **controller**, which he doesn't have and she doesn't
   either (probably Mercer's). She leaves repaired **but still leashed**, now knowing why.
4. **Mercer reacts SHOCKED and withholds missions while she's damaged** — the pressure that *motivates* the
   grind (a broken asset doesn't get sent out) and a recurring, tense beat.
5. **Kess is male.**
6. The **memory-flash tease** (the rescuer / the un-holdable name) **stays** — a light dangling hook.

**Net:** SALVAGE v2 is about **control**, not identity. The awakening / who-she-was / Cain / the real "chip"
at the Site all stay **reserved**. The Act-2 engine it hands off is concrete: *get the controller, cut the
chip, turn on Mercer* — the used→user turn, seeded here.

---

## 2. Frame, and the tests it has to pass

She comes out of the cell a **broken weapon** — her drain won't fire. She can't take a damaged asset to the
company (a broken asset gets reset or scrapped, and Mercer won't use her broken anyway). So she goes off the
books to **Kess** and grinds herself back to operational, one session at a time.

The three tests (unchanged doctrine):
1. **Content, not a bar.** The repair is a *grind* now — but **every session plays a distinct/varying scene**
   (the drain-test escalating as she heals). The gate is **repair-progress**, never coin-to-unlock. A
   repeatable loop that hands a scene each time is the RTS pattern; a bar you fill by re-seeing one scene, or
   by farming money, is the mopoga review. §3 is the load-bearing line.
2. **Has a verb.** The **supplicant / test-bench** verb (from v1): she's worked *on*, and each session she
   *tries her power* on a brought man. Now with a real arc (fails → fires).
3. **Leaves her changed.** She exits operational, **owing** a debt, and **leashed-and-knowing-it** — a
   concrete new want (the controller) she never had before.

---

## 3. The load-bearing line — why this grind is safe

The mopoga review said Vesper "boiled down to resource grinding rather than the adult content." The cure was
never "no grind" — RTS (the flagship) is built *on* repeatable loops ("the routine IS the porn pipe"). The
cure is **grind that delivers content.** So SALVAGE v2's grind is safe **iff**:
- **Every repair session plays a real, band-varying scene** (not the same clip re-seen to fill a bar).
- **Both ends of the coin loop are content.** Each session *costs* underworld `coin` (LO's call, 2026-07-16),
  and coin is earned ONLY through adult content already in the game — the brothel (+10/client,
  `3_activities.toml:1230`), the pit (+8/+20 a bout, `:1263`/`:1270`), Marsh's Sunday (+15,
  `5_scenes.toml:2191`). So the loop is **content → coin → content**: she works the underworld (scenes) to
  afford Kess (scenes) — no content-free step to click. This is the RTS *economy* (a currency routing between
  two content loops), NOT the mopoga farm (a bar filled by re-seeing one clip); it also repays the review's
  other half by making the underworld matter to the main spine.

Hold both and this is the RTS grind, not the mopoga grind. (The v1 "debt accrues, never coin-gated" model is
**superseded** — §10.)

---

## 4. The shape — a repeatable repair loop (reusing the captivity engine)

The chunk reuses captivity's proven structure: **one-time frame beats + a repeatable band-gated shelf.**

- **Frame one-shots** (auto-fire, `is_repeatable = false`): the berth intro/terms; the forensic read + the
  memory-leak (first session, once); the chip-snag (mid-repair, once); the **verdict** (at full repair).
- **The repeatable shelf** (the grind): a **"repair session"** activity at `kess_berth`, repeatable while she
  isn't fixed. Each session plays a **band-appropriate scene** (a man brought, her power tested), lowers her
  `core_strain` (progress), and adds to `kess_debt`. She keeps coming back until `core_strain = 0`.

This is the captivity shelf model **inverted**: captivity's scenes *raised* `core_strain` toward the break;
SALVAGE's sessions *lower* it toward repaired.

---

## 5. How progress works — `core_strain` drops through the bands (visible)

`core_strain` comes out of the cell **frozen at 96** = the sidebar's **"Core: Failing"** row. In v2 it is
**no longer flipped at the end** — it **drains down across the sessions**, so the player watches her heal in
real time through the bands the game already has (`0_systems_spec.toml:137-145`):

```
Core: Failing (72+, start 96) → Faulting (48-71) → Hot (24-47) → Nominal (1-23) → gone (0 = fully repaired)
```

- Each session applies **`core_strain -= 8`** (`op = "add"`, negative, `clamp = true`).
- **12 sessions** (LO's call) carry her 96 → 0 — band walk: Failing 1–4, Faulting 5–7, Hot 8–10, Nominal 11–12.
- At **0** the "Core: Failing"→…→"Nominal" row **vanishes** (renderer emits nothing at no-band, verified) and
  the **verdict** auto-fires.

⚠️ **Engine note (from the v1 build, verified):** a `set value = 0` effect survives (the location-exit apply
reads raw config, not the value>0 preview JSON — memory `trait_effects_json_is_preview_not_apply`); and
`op="add"` with a **negative** value is what actually lowers a trait — confirm the negative add compiles into
the `applyAndNotifyTrait` script (decode HTML entities when grepping the built passage).

---

## 6. How the test happens — the drain returns *with* the meter

Every repair session, a man is brought in and **she tries her drain on him.** The outcome is read straight
off her **current `core_strain` band**, so it escalates as she heals (same band-selection captivity used):

| Band (`core_strain`) | ~Session | The drain-test |
|---|---|---|
| **Failing** (72+) | 1–4 | **Dead.** He finishes in her; she reaches for the take — *nothing*. No pull. |
| **Faulting** (48–71) | 5–7 | **Sputters.** A flicker, a half-pull, then it drops. She *felt* it almost work — worse than nothing. |
| **Hot** (24–47) | 8–10 | **Catches.** It fires weak, pulls a thread of him, gutters out. First real proof it's coming back. |
| **Nominal** (1–23) | 11–12 | **Fires clean.** Full take. She's a weapon again. |

**Scene pool:** author **12 repair scenes — one per session, banded 4 / 3 / 3 / 2** (Failing / Faulting / Hot /
Nominal), each **one-shot + band-gated + `trigger_mode = "random"` (chance = 1.0)** — captivity's proven shelf
engine (`cell_use_inventory` et al., `5_scenes.toml:2616`) run in reverse (strain drops, not rises).
One-shot + band-gating = **zero verbatim repeat**: every session is a fresh scene. (This is +2 on the ~10 we
discussed — the clean no-repeat number for 12 sessions; trivially trimmed to 10 by letting the 4-long Failing
band re-see one scene.) The band fixes the drain-test outcome (dead/sputter/catch/fire); the man + the sex
vary per scene. Content ceiling = RTS-flat, crude, consensual (the brought men are willing test-bodies; no
degradation); reset the shared sex-loop traits on entry/exit of each session.

---

## 7. The one-time beats woven into the grind

- **Berth intro / terms** (first berth visit, once) — Kess (male) clocks her company steel, nearly ejects her,
  flips at the read (**custom / bespoke**, never "old"), names himself (Stranger→Kess handoff). Terms: it's
  session by session, each on the book (coin she doesn't have → owes). Dialogue-forward.
- **First session — the forensic read + the memory-leak** (once) — Kess reads the re-seated drain: *"somebody
  who'd had their fingers in you before, who didn't need to look."* And the **Tier-3 glitch-leak** (kept, per
  LO): mid-session her spine trips an involuntary memory — old smoke, the hand straight to the seam, one
  off-page syllable of a name that fits a lock. She reaches for it and can't hold it. (Reuses `beat_0042`'s
  devices; name never renders; NOT a chip fragment; sets nothing — a pure dangling tease.)
- **Mid-repair — the chip-snag** (once, ~Faulting/Hot band) — Kess catches on it: *"there's something down
  here I don't like — wired deeper than the rest. I'll want a proper look before I close you up."* Sets up
  the verdict; explains nothing yet.
- **At `core_strain` 0 — the verdict** (§8).

---

## 8. The verdict — the chip-as-leash reveal (Tier-3, once)

Fires when the repair completes (`core_strain = 0`). Kess delivers it (SPOKEN, dialogue-forward):

- **She's operational** — the drain fires clean, she's bought back.
- **But he found a control device** — a **governor / chip**, seated deep, older than the rest of the build.
  *Not damage — design.*
- **What it does:** it's a **leash.** There's a class of thing she's built so she *can't* do, and at the top
  of it is **the man who owns her.** She has never once been able to turn her power on Mercer. *That's not
  loyalty keeping her teeth off him — it's this.*
- **He can't pull it:** it's keyed — pull it wrong and it takes her with it. There's a **controller** (a key)
  somewhere; whoever holds it cuts it clean. Kess doesn't have it. Neither does she.
- **She already knows whose** — she doesn't ask; the shape of the answer is the man who signs for her
  (one rationed `thought_bubble`: *he's held the key the whole time*).
- **The close (cold, not hopeful):** she's a weapon with a lock on it, and the man who holds the key writes
  her orders. *That isn't despair — it's information. You can do something with information.* And under it,
  the four words from the cell still won't hold — *a different hunt, for a different day.*

**Mechanic:** by the verdict `core_strain` is already 0 (the sessions drained it), so the "Core: Failing" row
is already gone. The verdict sets **`core_sealed = 1`** → a standing sidebar row **`Leash: Uncut`** (relabel
of v1's `Core: Locked`; trait key unchanged). She walks out owing the `kess_debt` balance. Teleport to
`the_waterfront`.

---

## 9. Mercer — the shocked gate that motivates the grind

The piece that makes the grind make sense: **while she's damaged, Mercer will not use her.**

- **Mid-repair, at Mercer's hub (penthouse):** he's **shocked and refusing** — *"What happened to you. Where
  have you been. I can't send you out like this — go get yourself right."* No mission dispatched while
  `core_strain > 0` (or `salvage_done is_false`). Recurring while she's broken (the "shocked all the time"
  you wanted). This is the in-fiction reason she *has* to grind the repair: she can't get back to work
  until she's whole.
- **After the repair, first report-in:** he's **still wary** — what did you do, who touched my asset, why
  were you dark — and only *then*, grudgingly, hands her the next job. Seeds his suspicion (a later
  company-notices thread) and lands hard against the chip reveal (*he* holds her leash; now he's looking at
  *her* like she's contaminated — two parties newly wary, one holding the other's key).

⚠️ **Save-safety / extend-only:** the mid-repair "shocked/refuse" state must **gate on the SALVAGE flags**
(e.g. a new `salvage_entered is_true` + `salvage_done is_false` register-shift on Mercer's hub), **not** by
rewriting Mercer's shipped dispatch canvases. Do NOT retro-gate his existing mission flow in a
save-breaking way; add the shocked state as a higher-priority conditional layer.

---

## 10. The coin cost (REPLACES the v1 debt — LO's call 2026-07-16)

- **She pays as she goes.** Each repair session `costs = [{ trait = "coin", value = 20 }]` up front (the proven
  gate-toll pattern, `3_activities.toml:940`). Can't afford it → the "Start a repair session" link greys out
  until she earns more in the underworld (§3). ~**240 coin** over the 12-session grind.
- **`kess_debt` retires as a mechanic** — the key stays **declared** (save-safe; shipped saves keep it), but
  nothing feeds it and it drives no sidebar row. No accrual, no end-debt, no "you owe me."
- **Two accepted consequences of dropping the debt:** (1) Kess-as-creditor is no longer the Act-2 hook — he
  recurs as *the man who knows what's in her* (the leash-reader), on knowledge not money. (2) The verdict's
  close is *paid clean*, not *owing*.
- The v1 sixty-vs-forty prose-total bug is now impossible (no running debt to mis-state).

---

## 11. Kess — the fixer (now MALE)

- **Who:** an off-books dockside **synth-mechanic / ship-breaker** in the Reach, `kess_berth`. Reads bodies
  as **hardware, not people** (was "not women" in v1). Blunt, clinical, transactional; won't touch company
  work until a frame he can't put a book to walks in. Wants **coin** and the interesting problem.
- **Role:** the fixer AND the cold channel — he reads *what's in her* (the re-seated drain; the leash) and
  reports it, knowing **nothing** about Mercer's missions or the company's files (the v1 leak, cut).
- **Slug `npc_kess`** (already built). **NO schedule** (chunk-scripted at the berth; verified the schedule
  block must NOT sit under his `[[npcs]]` or it orphans Marsh's — memory
  `npc_schedule_orphan_on_insert`). Dialog speaker renders "Kess:"; "Stranger:" until he names himself.
  Recurs as the debt-holder. **All narration pronouns he/him.**
- Tolly / Reeves / the other test-bodies: narration-level, no `npc_` objects (quoted speech, like the
  captivity crew).

---

## 12. The re-launch (into the sandbox + Act-2 hook)

After the verdict teleports her to `the_waterfront`, she reports to Mercer (§9, the wary-then-dispatch beat):
Mercer hands her **Calloway** as a **plain company mission** — no build-file fusion, no personal stake stated
by anyone. She takes it. But now every order sits on a new floor: **her owner holds her leash.** Her real
drive, riding under the missions: **find the controller, cut the chip, turn on Mercer** (the used→user turn).
Calloway's *arc* stays the frontier (next chunk); this only drops the lead + the leash hook.

Quest cards: a Salvage **status** card during the grind (get yourself operational at the berth); a
post-Salvage **frontier** card reframed to the **leash** (*you're chipped; the man who owns you holds the
controller — find it and cut it*) + Mercer's Calloway job as a plain mission.

---

## 13. Register (owned by the author-game skill)

- **The repair sessions, the berth, the terms, Mercer's shocked beat** → **RTS-flat.** Terse, specific,
  crude, re-readable, real anatomical language; Kess's voice clinical (narrates a body like an engine).
  Dialogue-dominant wherever Kess/Mercer are present (target ≤ 1.5:1 narration:dialogue).
- **The memory-leak (first session) + the verdict** → **Tier-3, earned, once-only** — the two places the
  prose may spend. The leak reuses `beat_0042`'s devices (recurrence, not new purple).
- Third person throughout (`narration_person = "third"`, immutable). No Rule-5 impersonal-"you" similes.

---

## 14. Reserved / kept (do NOT spend)

- **Reserved (untouched):** the awakening / who she was, Cain (never on-page/named), the name "Vesper"
  (off-page), the Bastien-Cain alliance, the **real "chip"** at the Site (the finale) — Kess's device is a
  DIFFERENT object, deliberately **not** called "the chip" (→ `governor` / `control chip` / `leash`).
- **Kept:** the memory-leak tease (rescuer + un-holdable name); the cold-open (`beat_0048`, unchanged); the
  `kess_berth` lifecycle; the debt; the `core_strain`/`core_sealed` machinery; the Marsh-schedule fix.

---

## 15. Engine & save-safety

- **Reuses the captivity engine:** band-gated repeatable scenes on `core_strain` (`trigger`/`group` bands,
  `gte`+`lt`, exclusive) + the band-status sidebar row. The verdict is an auto-fire capstone at
  `core_strain = 0`.
- **Progress:** each session `core_strain -= ~16-20` (`op="add"` negative, `clamp=true`). The verdict fires on
  `core_strain = 0` (auto-fire, `is_repeatable=false`). ⚠️ confirm the negative-add compiles (per §5 note) and
  that the verdict's gate can't fire before 0.
- **New state (extend-only):** the repair-session canvases; the band-shelf scenes; the mid-repair Mercer
  shocked-layer; a `salvage_done`/progress guard for the verdict. Reuse existing `core_strain`, `core_sealed`,
  `kess_debt`, `salvage_*`, `npc_kess`, `kess_berth` — **no renames** (shipped saves survive).
- **Old-save cohort:** finished captivity, `core_strain = 96`, at the waterfront → the cold-open pulls them
  in; the grind carries them 96 → 0. New players the same after captivity.
- **Every new conditions block `version = "1.0"`;** gates on traits/flags, not triggerless flags.
- **Do NOT retro-gate Mercer's shipped dispatch** in a save-breaking way (§9) — layer the shocked state on top.

---

## 16. Build sequence (propose-first; one verified piece per turn)

Source phases → `merge_toml_phases.py` → `package_from_toml`. Never hand-edit `7_final_game.toml`.

1. **Systems:** relabel `core_sealed`'s row `Core: Locked` → `Leash: Uncut` (label only); confirm `core_strain`
   bands read as repair-progress. (`kess_debt`, `core_sealed` already declared.)
2. **Kess → male:** pronoun flip across the SALVAGE canvases + npc_kess desc ("not women" → "not people").
3. **The coin-gated repair-session activity** ("Start a repair session" @ kess_berth: `costs` 20 coin, gated
   `core_strain gte 1` + `salvage_done is_false`, repeatable) arming the **12-scene band-shelf** (one-shot +
   band-gated `trigger_mode` random, captivity engine in reverse; `core_strain -= 8` on each scene's exit;
   sex-loop reset). NO `kess_debt` feed (§10).
4. **The frame one-shots:** berth intro/terms (rework from v1's Kess intro); first-session forensic read +
   memory-leak; the mid-repair chip-snag.
5. **The verdict** (chip-as-leash reveal; `core_sealed=1`; teleport).
6. **Mercer's shocked gate** (mid-repair refuse layer + the wary-then-dispatch re-launch).
7. **Quest cards** reframed to the leash.
8. **Retire/adapt v1 content:** the v1 Stage A/B/verdict/re-launch canvases are reworked or replaced; keep
   the cold-open. Update `design_book.md` (`## Salvage` → v2) + `authoring_state.json` + this doc's status.
9. **Merge → green build → live-test → rebuild `--dev --debug` → commit + push over `a2ec95f`.**

---

## 17. Verification plan

Green build each piece. Headless live-test:
1. **The grind delivers content, not a bar** — assert each session plays a scene, no action spams a number
   with no content, the gate is repair-progress (not coin).
2. **Progress is visible** — `core_strain` drops per session; the sidebar band steps Failing→…→Nominal→gone.
3. **The test escalates** — the band picks the drain-test outcome (dead→sputter→catch→fire) correctly at each
   band; the scene pool rotates (no verbatim repeat back-to-back).
4. **The verdict fires once at 0** — the chip reveal; `core_sealed=1` lights `Leash: Uncut`; teleports out.
5. **Mercer's gate** — mid-repair he refuses/reacts shocked (no mission while `salvage_done is_false`);
   post-repair he's wary then dispatches Calloway; his shipped dispatch not save-broken.
6. **The debt** — accrues per session; the prose total matches the accrual (no sixty-vs-forty).
7. **Register** — 0 second-person leaks; narration:dialogue ≤ ~1.5:1 on Kess/Mercer scenes; Kess narrated
   "he" throughout; 0 stray "Calloway file room / build file" in Kess's or Reeves' mouth.
8. **Marsh still scheduled** @underworld_brothel, Kess unscheduled (don't regress the `a2ec95f` fix).
9. **Zero JS errors.**

---

## 18. Dials — RESOLVED with LO (2026-07-16)

1. **Grind length** — **12 sessions**, `core_strain -= 8` each (96 → 0).
2. **Pacing** — **no energy cost.** Coin is the only gate; the time-to-earn-coin (brothel/pit/Marsh each
   +120 min) *is* the days-long ordeal — no separate energy meter.
3. **Scene pool** — **12 scenes, one per session, banded 4/3/3/2**, one-shot + band-gated for zero repeat (§6).
4. **Sidebar label** — **`Leash: Uncut`**.
5. **Cost per session** — **20 coin, flat** (~240 total; kept vague in prose).
6. **Berth post-repair** — **locks** (defer Kess's return to the chunk that re-opens him).

The one reversal from the first lock: repair is **coin-cost-per-session**, not debt-accrual (§3, §10).
Everything else holds.

---

## 19. What this supersedes

- **v1** (`design_salvage_the_repair.md`): the tight 2-scene bridge + the awakening/build-file verdict +
  female Kess + the Calloway-file fusion. **Superseded.** Its cold-open, Kess/berth, debt, and
  `core_strain`/`core_sealed` mechanic carry forward; its Stage A/B, verdict, re-launch, and quest-card
  reveal are **replaced** by this doc.
- The **built** v1 canvases (`salvage_stage_a/b`, `salvage_verdict`, `salvage_relaunch`, the quest cards) are
  reworked or retired at authoring; the cold-open (`salvage_body_wont_hold`) and the Kess intro survive
  (reworked for male Kess + the session terms).
