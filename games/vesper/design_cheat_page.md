# Vesper — Locked Design: The Ledger (the player cheat page)

> **What this doc is.** The design record for Vesper's player-facing cheat page — the first one any game in
> this repo will ship. Contents, the free/paid split, the step sizes, and the engine work it needs.
>
> **Provenance.** Built from three studies run 2026-07-25/26 against primary sources: the **supply** side
> (built HTML of 28 top mopoga games, 12 dissected — `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/cheat_page_study.md`),
> the **demand** side (2,389 cheat comments / 39,481 likes classified — same dir), and a 6-dimension
> **friction audit** of this game's TOML.
>
> **Revision 2 (2026-07-26).** Rev 1 was fact-checked and stress-tested against the repo before any of it was
> built. It had **two blockers, two content-deletion paths, and one false paid claim**; §13 lists exactly what
> changed and why, because the errors are instructive. Every number below was recomputed and every engine
> claim re-verified at the cited line.
>
> **Status:** decisions LOCKED (§1); design **LOCKED pending the three open items in §11**.
> `design_book.md` and `authoring_state.json` are **untouched** — folding in is propose-first. **Nothing is
> authored into `toml_phases/` yet.**

---

## 1. The decisions — LO's calls, and what they rest on

| # | Decision | The evidence |
|---|---|---|
| **D1** | **Ship a cheat page. No cheat codes, ever.** | 73% of all cheat-comment like-weight (28,906 of 39,481) is people hunting an access code, naming no effect. A code field draws ~42 code-questions per 1,000 comments; a button or checkbox draws ~11 — Degrees of Lewdity and Course of Temptation get **3 each** across 2,289 and 2,617 comments. 29% of code-asks are "the old code stopped working." |
| **D2** | **Two builds.** Free build shows the page; paid build has the rows live. | Build segregation is the **only** enforcement that held in the corpus. All four monetized code-gates examined were bypassable from the shipped file. 523 comments across 12/12 batches are players handing each other codes. |
| **D3** | **Nothing free** — no grants, no guidance, in the free build. | LO's call, 2026-07-26. Overrides the study's "free goodwill" recommendation. Consequence accepted in §10. |
| **D4** | **The free page shows row LABELS, not requirement text.** | A label (`Renner +10 🔒`) is a product listing and teaches nothing; requirement text teaches the game and is paid. |
| **D5** | **The game fixes are a later release**, not this page's job. | LO's call. §10 and §11.2. |

**Anti-cheat risk:** 15 comments / 44 likes in 2,389 — **0.11% of like-weight**, downvoted where it appeared,
and about a third was players reporting cheating broke their own save. One studied game was *downrated for
removing* cheats. No measurable social cost.

---

## 2. What needs cheating in Vesper — derived, and what each grant COSTS the player

Recomputed from `7_final_game.toml`. **Rev-1 error corrected:** rev 1 enumerated only `gte` gates. An
**`lt`-only gate is a window too** — it gates the *alternative* route, so raising a trait past it deletes
that route. A systematic parse finds **10 `gte`+`lt` windows and 19 `lt`-only exclusive blocks** on these six
traits. That changes two rows materially.

| Trait | Gates reading it | Why a valve | Step | What raising it DESTROYS |
|---|---|---|---|---|
| `coin` | **no gate** — spent via `costs` | Starts **0** (`:349`); underworld toll **5** (`:2555`), charged on **every** entry (`:2551`); all three faucets are behind that door (brothel +10, pit +8/+20, Marsh +15 — each resolved to its location). Salvage repair = 12 × 10 (`:7128`). | see §5 | Nothing directly — **but it launders** (below) |
| `fighting` | 10, 15, 25, 30, 40 (`gte`); **`lt 30` band in `activity_train`** (`:1965`) | 15 forces the underworld door; 30 opens hard pit bouts (+20 vs +8); 40 clears yard guard 3. | **+5** | Past 50, `activity_train`'s only bands (`lt 30`, `[30,50)`) both fail → **the Drill canvas renders with no choices** |
| `stealth` | 10, 25, 30, 40 (`gte`); **9 `lt` blocks** (`:2168`, `:2175`, `:2182`, `:2204`…, `:2240`…) | Same yard-3 ceiling; same +1 plateau above 30. | **+5, hard-capped at 9** | ⚠️ The yard gates every **non-stealth** route on `stealth lt N` per guard. Buying stealth deletes "Take him down", the **Tier-5 emitter scene** (`yard_crawl.weapon_scene`, `:2284`) and "break and run" at that guard. Only 3 guard encounters exist per save — a stealth-40 player **can never reach the emitter scene at all** |
| `npc_renner.corruption` | 0, 10, 20, 30, 40, 50 (`gte`) + **5 windows inside RANDOM canvases** | Rungs give **+2** (`:3671`, `:3686`, `:3705`); exits cost **180 min** against a 540-min window (09:00–18:00) → **3/day, 8-day floor, ~24 clicks**. Mandatory: `names_known` is set only at the drain and gates the whole Underworld Hunt. Calloway's identical arc costs 6 rungs at +3 to a gate of 18 — Renner is an un-retuned early value. | **+10** | ⚠️ Five bands sit in `trigger_mode="random"` / `[[trigger.substitutions]]` canvases at chance 0.10 / 0.35 / 0.70, `max_triggers_per_day = 1` (`:3777-3792`, `:4521-4533`). There **being in band is not enough — you must roll while in band**, so *any* step can skip them |
| `energy` (Charge) | **no gate** — spent via `costs` (15/action) | `activity_charge_up` is free, unscheduled, +100 — so this is convenience, not relief. | set 100 | Nothing |
| `hygiene` (Condition) | **40**, on exactly **one** choice | **Rev-1 error:** the single gate is on "Ride down to the Reach" (`:1563`) only. Its sibling to the Underworld has no hygiene clause (`:1568`), and the gate's own "Up to the Reach" (`:1714`) has **no conditions at all** — so a filthy Wren reaches the docks in two clicks and coin-grinding never meets the gate. What hygiene really throttles is the **Reach/cover lane** (Renner). | — | **Row cut — see §5** |

### The band-safe rule, stated properly

A `+N` step is band-safe **only against deterministic gates**. For `trigger_mode = "random"` and
`[[trigger.substitutions]]` bands, reachability is *chance × dwell-time-in-band*, so no step is safe — the
player has to linger in the band and roll. Renner's two ambient canvases are the counter-example that kills
the general claim. **This belongs in the skill, not just here** (§12).

### Coin launders past every cap

`underworld_market_shop` is `is_repeatable = true` (`:2911`) and sells `fighting +5` for 40 coin (`:2927`)
and `stealth +5` for 30 coin (`:2933`) — **with no `cap` and no `clamp` on either effect.** So one
`Coin +120` converts to +15 fighting or +20 stealth, unbounded and repeatable, defeating any cap this page
sets, and past 40 it deletes the yard routes above. This is a **pre-existing exploit** in the game, not
something the page introduces — but the page makes it one click wide. See §11.1.

---

## 3. The two builds

One TOML. One switch. **Rev-1 blocker corrected:** rev 1 said the free build would "not emit the grant rows,"
which would have deleted their labels too — leaving the title, the pitch line and `Close`, with nothing
between. The mockup and the mechanism contradicted each other.

**The mechanism that actually works, using what the engine already ships:** keep every grant choice, and when
`cheat_grants = false`, force its condition false and strip its `effects`/`costs`. The engine reads
`show_when_locked` and `locked_text` per choice (`v2.py:12706-12707`), so each row renders as a **greyed
label** — which is exactly the padlock row §4 wants. This game already uses that path correctly at `:1633`,
`:1710`, `:3664`.

**Why condition-gating alone is not enough:** `games/vesper/output/index.html` is git-tracked in
`storygen-beep/Story-Gen`, which `gh repo view` reports `PUBLIC`. A gated row's effects are still in the file.
The switch must **strip the effects**, not just gate the row. (A determined person on a public build still
wins — that costs us nothing, unlike a code that needs rotating and a support thread.)

---

## 4. The free build — the page exists and grants nothing

**Do not label the row "Cheats."** The corpus trap: a game whose sidebar carries a row literally labelled
*Cheats* that is a bare link to a donation pitch — *"the word 'Cheats' is being used as ad inventory in the
sidebar."* A cheat-shaped affordance that does nothing reads as a bug, not an offer.

```
THE LEDGER

She keeps her own numbers. Supporters get to change them.

    Coin              🔒
    Fighting          🔒
    Stealth           🔒
    Renner            🔒
    Charge            🔒
```

Five padlocks — labels only, no thresholds, no places, no routes (D4).

**No in-page Patreon button.** The sidebar already renders `<<patreonButton>>` on every passage, and quest
card D already closes with a "Support Us" line (`:10603`). A third CTA on a page that grants nothing is what
turns the page into the ad-inventory failure above. The padlocks point at a CTA that is already on screen.

---

## 5. The paid build — five rows

Register: **flat and mechanical.** 0 of 12 studied games write diegetic option labels; the container carries
the fiction, the rows stay legible.

| Row | Requirement text (paid) | Effect |
|---|---|---|
| `Coin +25` | five trips through the gate, or two salvage sessions | `coin` add 25 |
| `Fighting +5` | the door at 15 · hard bouts at 30 · the yard at 40 | `fighting` add 5, cap 40, clamp |
| `Stealth +5` | the yard at 40 — **but the fight, emitter and run-away routes close as it climbs** | `stealth` add 5, cap 9 *(see below)* |
| `Renner +10` | opens the anal pose in the office loop — in cover, carrying the charged drain. The rungs still have to be run. | `npc_renner.corruption` add 10, cap 50, clamp |
| `Charge → full` | — | `energy` set 100 |
| `Close` | — | exit to the room |

**Three rows changed from rev 1:**

- **`Wash` — CUT.** `activity_wash` already exists **at the same room**, free, repeatable, hygiene → 100,
  30 minutes (`:2986-3013`). The row would have sold a 30-minute saving on a free action in the room the
  player is standing in.
- **`Coin +10` → `Coin +25`.** The toll is 5, not 10, and it is charged on *every* entry; a session is 10.
  `+25` maps to something a player can name.  **`Coin +120` cut** — it is the laundering channel (§2) and
  the row is repeatable anyway.
- **`Stealth +5` capped at 9.** Guard 1's alternative routes are gated `stealth lt 10`. Capping below 10
  keeps every yard route alive and lets the yard teach the rest. If LO would rather sell the full ladder, the
  requirement text must say what closes — that is §11.3.

**Renner's text was false in rev 1.** Corruption 50 opens nothing on its own: the drain sits behind a flag
chain the page deliberately will not grant — `renner_flirts_back` (set only by the Flash rung, `:3690`) →
`renner_oral_once` (`:4070`) → `renner_fucked_once` (`:3730`), and the anal pose additionally needs
`cover_dockhand` equipped (`:4198-4201`). Selling a false claim is worse than selling nothing.

Shape of every grant row — each clause load-bearing:

```toml
[[canvases.nodes.exit_block.choices]]
text                     = "Fighting +5"
targetType               = "node"
nodeId                   = "base"    # self-loop — stay on the page, gates re-evaluate in place
time_progression_minutes = 0         # the choice default is 3; ten clicks would burn half an hour
show_when_locked         = true      # at cap, the row greys out instead of lying
locked_text              = "Already as sharp as this will make her."
conditions = { version = "1.0", items = [                       # the at-cap guard
  { type = "trait", subject = "player", trait_key = "fighting", operator = "lt", value = 40 } ] }
effects = [ { targetType = "player", trait = "fighting", op = "add",
              value = 5, cap = 40, clamp = true } ]              # BOTH — see §8
```

**Every row needs the at-cap guard.** Without it, `add 5, cap 40, clamp` at fighting 40 is a lit button that
silently does nothing — the mirror of the corpus failure the study flagged, and the version that generates
support threads. **The page must not itself cost time or energy** (named explicitly in the demand data).

---

## 6. Where the page lives — the rev-1 blocker

**Rev 1 said `wren_room`. That was wrong, and it broke the page's own purpose.**

`wren_room` sits four levels inside the Spire (`spire_plaza → atrium → wren_floor → wren_room`), and
`spire_plaza` has **no `entry_from`** — it appears in no location's nav. The only two routes in are
`activity_travel_to_spire` (`:1635`) and `activity_travel_from_gate` (`:1711`), and **both are gated
`archive_1a_done is_false`**. The moment that flag sets, ~47 Spire canvases seal — and the cheat page with
them. Rev 1 justified the Charge row as "the safety net for the one place the game strands a player," while
siting the page where it is off the map at exactly that moment. `captive_room` is a second such hole (a
fourth nav root, `:1111`).

**Resolution — the sidebar page is a prerequisite, not an upgrade.** A zone-independent surface is the only
one that survives both seals, and the demand data is emphatic that reachability is most of a cheat page's
value. Blockers to clear first:

- The build ships `setup.tips_page = {}` and the 💡 link is gated `<<if setup.tips_page && setup.tips_page.content>>`
  (`v2.py:15985`), so the button never renders today. No Vesper phase authors it; the `author-game` skill has
  **zero** hits for `tips_page` — a doctrine gap, not a Vesper slip.
- It means raw SugarCube inside a TOML string that **no validator checks**, and a non-navigating write there
  needs `setup.commitMoment()` or the change is lost on save/refresh. **⚠️ verify at build.**

**Fallback if the sidebar route can't be made safe:** emit the canvas at **`underworld_strip`** instead of
`wren_room` — reachable post-seal, and it is where the coin economy and the salvage actually live. Then drop
the Charge row's post-Archive rationale to "convenience," honestly.

**The self-loop needs no verification** — rev 1 flagged it, unnecessarily. This game already ships it:
`loop_renner_office_sex` node `base_doggy_r` carries a choice targeting its own `nodeId` (`:4229-4231`), and
its finisher only opens once `loop_npc_pleasure gte 50`, reachable **only** by repeated self-loop clicks.

---

## 7. What is NOT on this page

| Excluded | Why |
|---|---|
| **Money / Credits** | Starts at **50** (`:336`); one other writer (+8, `:3812`); **no gate reads it**. It has no `[[traits.labels]]` entry, so it is *not* hidden — it shows as a raw row in the Traits dump. A grant would move a number the player can see and nothing consumes. `coin` is the real wallet. |
| **Day-skip** | ~3 mentions in 2,389 comments; the sidebar already ships wait buttons. |
| **Items** | ~3 asks in 2,389 — *"not one request for a specific item."* Vesper's items are story objects. |
| **Story flags** | Causality; the flag-chain validator does not protect us here. Also why Renner's row cannot sell the drain outright (§5). |
| **`*_stage` / counter traits** | Best-supported finding in the supply study. Vesper has 24 hidden internal counters; the page touches none. |
| **Scene jumps** | Player/dev band split. Ours stay in `<<devJumps>>` behind `dev_mode_enabled`. |
| **`core_strain`** | Top band is deliberately open-ended (no `max`) — no honest cap exists. |
| **`hygiene`** | Free wash already in the room (§5). |
| **Relation ladders** | Cheap already — Colm **7 clicks** (meet +3, three drinks +3, three kisses +4), Renner 7, Calloway 5. If ever added: Colm **+4**, Renner +21, Calloway +15. |
| **The post-Archive cage** | No grant reopens a location that is off the map (§6). Game-fix territory. |

---

## 8. Verified engine facts and traps

Re-verified this session; rev 1's citations were right on substance but pointed at neighbouring code paths.

- **On the CHOICE path, `clamp` defaults to `False` and `cap` to `None`** — the choice path calls
  `self._emit_trait_effects_inline(...)` at **`v2.py:12141`**, whose defaults are `clamp_flag = eff.get('clamp', False)`
  (**`:13089`**) and `cap = eff.get('cap', None)` (**`:13091`**). The JS helper *would* default clamp to true
  (`:5616`) but the emitter always passes an explicit `false`. **Write both on every banded row.** A cap
  applied later cannot repair an overshoot. *(Rev 1 cited `:12254`/`:12322`/`:12949` — rejection-effects, the
  loop-back duplicate, and the location-exit path respectively. Same fact, wrong paths.)*
- **The per-choice time default is indirect** — `default_time = config.get('default_time_progression', 3)`
  (**`:12686`**) consumed at **`:12700`**. Resolves to 3 for Vesper, but an `exit_block`-level
  `default_time_progression` would silently change it. *(Rev 1 cited `:12860`, the location-exit path.)*
- **`show_when_locked` / `locked_text` are read per choice** — `v2.py:12706-12707`. This is the padlock row.
- **A `conditions` block without `version = "1.0"` FAILS OPEN** — grants access, no build error.
- **The 💡 page is gated on non-empty content** — `v2.py:15985`; the build ships `setup.tips_page = {}`.
- **The built game is public** — `games/vesper/output/index.html` tracked in a repo `gh` reports `PUBLIC`.
- **⚠️ `merge_toml_phases.py` reads a HARDCODED file list** — `PHASE_FILES` at `scripts/merge_toml_phases.py:44-56`
  is a literal list (0–6 plus `8_phone.toml`); there is no glob and no directory scan, and the loop warns only
  about *missing* known phases, never unknown extras. **A new `8_cheat_page.toml` would never be merged, the
  merge would report success, and the canvas would silently not exist.** `8` is also already taken.
  → **Author the page into `3_activities.toml`** (its honest home — a solo activity), or add the filename to
  `PHASE_FILES` first.

---

## 9. Engine work — the one change worth making

**`[settings] cheat_grants = true|false`** (name open), consumed by the generator: when false, each cheat row
keeps its `text`, `show_when_locked` and `locked_text`, but its `effects`/`costs` are **dropped** and its
condition forced false — so the row renders greyed (§3).

- **Buys:** the two-build model from one authored source. No drift, no duplicated page. Reusable by every
  future game, and it is what makes D2 real rather than cosmetic.
- **Cost:** small — one setting through the importer, one filter in the choice emitter.
- **Rejected:** dropping the choices entirely (deletes the labels — the rev-1 blocker); condition-gating
  alone (leaves the effects in a public file).

Deferred, worth it later: a declarative `[[ui.cheat_page.grants]]` block, so grants become validated data and
the undeclared-trait hard-fail plus cap/clamp rules apply automatically.

---

## 10. The accepted consequence of D3 + D5

Vesper's #1 friction is the underworld door: coin starts 0, the toll is 5, every faucet is behind the door,
and the alternative — "Force past him," `fighting gte 15` — **has no `show_when_locked`, so the choice renders
as nothing at all.** A first-time player sees a toll they cannot pay and "Turn back." The only fighting
trainer is back in her room and nothing points there.

Under D3 the page gives that player nothing; under D5 the fix ships later. **So until that release, a free
player can sit at that door with no visible way through.**

**Recommendation, LO's call:** pull that one fix into this release. It is two lines using a pattern this file
already uses correctly (`:1633`, `:1710`, `:3664`), it is not "giving away a cheat" — it makes an existing
choice visible — and it is the difference between a free player buying a tier and a free player concluding
the game is broken. Tracked in §12 so an open decision doesn't ship as a silent no.

---

## 11. Open decisions

1. **Cap the market's stat sales?** `underworld_market_shop` sells `fighting +5` / `stealth +5` with no cap
   and no clamp (`:2927`, `:2933`), repeatable — a pre-existing exploit that also launders coin past this
   page's caps (§2). Adding `cap = 40, clamp = true` to both is a two-line game fix. Recommend yes.
2. **Does the door fix ride along?** §10. Recommend yes.
3. **Stealth row: cap at 9, or sell the full ladder with a warning?** Capping at 9 preserves every yard route
   including the Tier-5 emitter scene. Selling the full ladder needs the requirement text to say what closes.
   Recommend cap 9.
4. **The container's name.** "The Ledger" is a placeholder that fits her. LO's pick.
5. **Hide the page until the cold open ends?** The #1 studied game hides its cheat glyph until
   `$game.introFinished` — the one thing its menu cannot skip. Cheap for us. Recommend yes.

---

## 12. Ship checklist

- [ ] Page authored into **`3_activities.toml`** (NOT a new `8_*.toml` — `PHASE_FILES` is hardcoded, §8),
      merged via `scripts/merge_toml_phases.py`, and the canvas **confirmed present in `7_final_game.toml`**.
- [ ] Surface survives both zone seals (§6) — sidebar route, or sited at `underworld_strip`.
- [ ] Every banded row carries **both** `cap` and `clamp = true`; **every** row carries
      `time_progression_minutes = 0` and an **at-cap guard** + `locked_text`.
- [ ] Steps: fighting +5 (cap 40), stealth +5 (cap 9), Renner corruption +10 (cap 50). **No set-to-max on a
      banded trait.** Renner's requirement text names the cover + the charged drain, not "opens the drain."
- [ ] No `flagEffects`, no `questEffects`, no `*_stage` write, no scene jump anywhere on the page.
- [ ] Any `conditions` block carries `version = "1.0"`.
- [ ] Live-tested in the built game: each row moves its number, the sidebar reflects it, the clock does not
      advance, a Save/refresh keeps the change, and a maxed row greys instead of doing nothing.
- [ ] Free build verified by **grep on the built HTML** — the grant *effects* absent, the *labels* present.
- [ ] Door fix (§10) shipped or explicitly deferred **in writing**.
- [ ] `--video-folder`, no `--dev`, no `--debug`; `grep -c 'IMAGE MISSING\|VIDEO MISSING'` == 0.
- [ ] Folded into `design_book.md` + `authoring_state.json` (propose-first).
- [ ] **Skill fixes**, tracked separately — without them the next game repeats these defects:
      `ship-gate.md` §3 (four of its eight claims refuted by the supply study), the **`lt`-only gate is a
      window** rule, the **random/substitution bands are never step-safe** rule, and `tips_page` doctrine.

---

## 13. What rev 1 got wrong

Kept deliberately — these are the failure modes the skill should learn, not just this page.

| Rev-1 claim | Reality |
|---|---|
| Author as a new `8_cheat_page.toml` | **Blocker.** `PHASE_FILES` is hardcoded; the file is never merged and the merge still reports success. |
| Free build = don't emit the grant rows | **Blocker.** Drops the labels with them — the free page would have been empty. Real mechanism: keep the choice, strip effects, force the condition false, let `show_when_locked` grey it. |
| Page at `wren_room` | Seals post-`archive_1a_done` along with ~47 Spire canvases — at exactly the moment the Charge row was justified by. |
| Six rows / seven listed | Internal inconsistency; now five. |
| `Wash` as a paid row | A free wash already exists **in the same room**. |
| "his drain opens at 50" | False — a flag chain plus equipped cover also gate it. A false claim in the paid band. |
| Step sizes are band-safe | Only for **deterministic** gates. Missed 19 `lt`-only blocks and 5 random/substitution bands. |
| Stealth +5 is safe | Raising stealth **deletes** the yard's fight / emitter / flee routes; a stealth-40 player can never see the Tier-5 emitter scene. |
| `coin` has no bands to break | It launders — the market sells uncapped `+5` stats for coin. |
| Money has one writer, zero readers | Starts at 50, and it is visible in the Traits dump (no labels entry). |
| Clamp/cap at `:12254`/`:12322`/`:12949`; time at `:12860` | Right facts, wrong code paths. Choice path is `:12141` → `:13089`/`:13091`; time is `:12686`/`:12700`. |
| ⚠️ verify the self-loop | Unnecessary — already shipped in this game at `:4229-4231`. |
