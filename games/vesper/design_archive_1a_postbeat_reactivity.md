# The Archive 1a — Post-Milestone State Reactivity (design + build doc)

**Status:** Phase 1 + Phase 2 BUILT (rev 88, uncommitted). Skill/doctrine fix (§7) DONE (author-game CHANGELOG 2026-07-23, uncommitted). Whole thread complete.
**Owner:** ENI · **Game:** `games/vesper` · **Last updated:** 2026-07-23 (book_revision 88)
**Scope:** how NPC interactions and the world change after the two one-way milestones of The Archive 1a — the Calloway drain and the 1a blowup — so the game stops offering pre-milestone content as if the turning points never happened.

---

## 0. Why this doc exists

LO's observation (paraphrased): *after a one-way beat — Vane hands over the docs and it's "run" — the player can still walk back and interact normally. Same with Mercer. It sounds wrong.*

He's right in principle, and a read-only audit (4 parallel readers, file:line evidence) placed it precisely. This doc is the single source of truth for: the diagnosis, the design decision, what has already shipped, what still needs building, and the systematic fix so it doesn't recur in the next game.

---

## 1. Diagnosis — where the defect lives

The audit corrected the naive read. The specific example LO named (**Vane**) is the one place Vesper already handles this correctly; the real offenders were **Mercer** and **Calloway's whole floor**.

- **Engine — innocent.** All nine gating primitives exist and work: canvas `trigger.conditions`, choice-level `conditions` (+ `show_when_locked`/`locked_text`), `[group]` node-body variants, substitution-bucket conditions, `npc_at_location` presence, location `entry_conditions`, one-shot consumption (`is_repeatable=false`), quest/stage gating. Nothing is missing at the engine layer.
- **Vesper — half-applied.** The author *did* close **Vane** correctly (his floor small-talk drops on `vane_confirmed`; his night observation self-gates; the blackmail is one-shot). That proves the primitives are usable. But the standing **Calloway** floor and the **Mercer** hub were left live — attention went to the capstones, the everyday surfaces got missed.
- **Skill — a real, partial gap.** `author-game` teaches the *intent* (content-framework.md §3C/§4B/§4E: "what old moments are retired… dead before this night, alive after") and the *capstone* self-retire (lanes.md:293). It has **no named pattern for retiring/mutating a STANDING Lane-1 hub** (+ its walk-in pool / drain / work-grind / floor cluster) after a one-way terminal beat — and presence-floor doctrine mildly *tolerates* a spent hub standing. This overlaps the known-HIGH "post-capstone infra / frontier steady-state" sandbox gap. **A correct skill would have prevented the Calloway floor** → the fix belongs in the skill too (§7).

---

## 2. The design decision (the fiction we agreed)

After the 1a blowup, Wren is **blown**. The pulled file carries "a deep-vault flag with my asset's fingerprints on it," and it climbs to Chairman Vance. The company now knows an asset breached the archive — **and that asset is her.** She is no longer a hidden mole; she is the target of the internal rogue-hunt she was helping run.

Consequences we locked:

1. **She and Mercer run to the underworld.** Mercer holds the controller for the leash in her core — she can't cut it and can't lose him — so she extracts him and takes the file. They flee the Spire together.
2. **Calloway is her enemy now — structurally, not by a personal betrayal beat.** He *runs the internal hunt for the rogue*. After the blowup there's a fresh breach on his floor and he's hunting it — hunting her. The man she drained for the vault location is exactly who would catch her. (No scripted "Calloway realizes" scene; the memory-wipe makes that incoherent. His enmity is the company net closing, which he leads.)
3. **The whole company turf closes to her.** Not a per-room edit — she physically can't be there. The Spire seals behind her.
4. **The stakes: caught = killed or reset (memory-wiped).** The tech she spent the game using on others is now the fate hanging over her. Delivered as *threat* (the run beat + the sealed-door messages), NOT as a built capture/reset system in 1a.
5. **The underworld base is deferred to 1b.** For now, the blowup is the end of built 1a content; she runs, the turf locks, and 1b (the Bastien deal / the leash trade) will happen off the Spire's ground with her new base.

---

## 3. The two-milestone model

Two different one-way moments drive two different sets of changes. They are **not** the same beat and must not be wired the same way.

| Milestone | Flag / trait | Fiction | What changes |
|---|---|---|---|
| **A. Calloway drain** | `calloway_drains_done gte 1` (trait) | She owns him — his memories, the vault location, a permanent leash. Still undercover; nobody knows. | Calloway's **personal** surface flips from *earn / seduce* to *he's yours*. Local to Calloway. The floor is still a working office. |
| **B. The blowup** | `archive_1a_done` (flag, set by `cap_1a_close`) | She's exposed; Chairman inbound; she and Mercer flee. | The **entire Spire turf** seals; she runs to the underworld. Everything company-side goes off her map at once. |

Sequence: drain (A) → docs first-look → Vane blackmail → **blowup (B)**. There is a window between A and B where she still walks the file room undercover — that window is what Phase 1 governs.

---

## 4. Phase 2 — THE SPIRE SEAL — **BUILT (rev 87, uncommitted)**

**Design insight that made this cheap:** the whole Spire is one tree rooted at `spire_plaza`, reachable **only** via the car up from the Reach. Cut the ride → the entire campus (plaza / atrium / penthouse / vance_securities / docs_department / docs_vault / wren_floor / wren_room / cradle) is unreachable in one move. No per-canvas edits needed — Mercer's hub+serve+finisher, Calloway's drain-again+work+rounds, and the docs floor all die because she can't reach them.

**The 5 edits (all shipped):**

| # | File | Change |
|---|---|---|
| A | `5_scenes.toml` cap_1a_close exit (~6712) | Exit re-pointed `penthouse` → **`the_waterfront`** (was leaving her standing in the room she flees). Closing prose plants the descent + seal: *"The Spire locks shut behind them… No ride back up. Only down, from here."* |
| B | `3_activities.toml` `activity_travel_to_spire` "Ride up to the Spire" choice | `show_when_locked=true` + `locked_text` (security line) + `conditions {archive_1a_done is_false}`. Blown → greyed with the message; the "Down under the docks — the Underworld" choice stays live. |
| C | `3_activities.toml` `activity_travel_from_gate` "Ride up to the Spire" choice | Same treatment. Blown → greyed; "Up to the Reach" stays live. |
| D | `1_metadata_and_locations.toml` `penthouse` | Backstop `entry_conditions {archive_1a_done is_false}` + `blocked_message` (defense-in-depth). |
| E | `1_metadata_and_locations.toml` `vance_securities` | Backstop: added `archive_1a_done is_false` to existing `salvage_relaunched is_true` items (AND). |

**Why `show_when_locked` is safe here:** the `locked_text` is written FOR the post-blowup locked state, so it displays exactly when it's true — never stale. (Contrast the toml-gotchas trap: a *consumed* `is_false` clause carrying `show_when_locked` leaks a PRE-milestone message post-consumption. Not the case here — this gate never re-opens.)

**Verification (done):**
- Merge: `validation: OK`; package: `✓ Validation passed` + `✓ All flag chains valid`.
- Headless live test (Playwright): blown state removes the ride-up active link at **both** chokepoints, the security message is on-screen, only the down/reach choice is clickable; undercover the ride works normally. Ejection link `[[…->Location_the_waterfront]]` baked into the blowup passage.

**Resolved by the seal (no further work):**
- **Mercer** — hub + serve + finisher: all unreachable post-blowup. He's the "unchanging owner" by design, so he needs nothing pre-blowup. **Fully resolved by Phase 2.**
- **Make the rounds** (`chat_the_floor`) + the 4 teammate walk-ins + 3 floor ambients: unreachable post-blowup. Undercover they're fine. **Resolved by Phase 2.**
- **Docs floor** (Vane, Enns): unreachable post-blowup.

**Accepted consequence — day/recharge freeze.** The cradle carries the day-router (`activity_recharge` "Power down", advances the day) and all recharge (`activity_charge_up`, weapon reloads), and it's inside the sealed Spire. Post-blowup the day cannot advance and Charge cannot refill. This is **safe as the end-of-1a wall**: 1b is unbuilt, the base is deferred, and nothing crashes (she can still move through the underworld — energy going low degrades, never hard-locks). **1b's underworld base must carry a new recharge/day-router.**

---

## 5. Phase 1 — CALLOWAY "HE'S YOURS" SWAPS — **BUILT (rev 88, uncommitted)**

Governs the window **after the drain, before the blowup**, where she revisits the file room undercover. Gated on the trait `calloway_drains_done gte 1` (validator-exempt). **3 edits shipped** (all `5_scenes.toml`): the two seduction rungs "Get close to him" (5382) + "Take him in your mouth" (5397) HIDE post-drain (`show_when_locked` removed + `calloway_drains_done lt 1` added — hide, not grey, to dodge the stale-locked_text trap); the "Talk to him" `.talk` node (5445) and `work_the_case` base node (5488) `[group]`-swap courtship → possessive prose. The optional card 5 was **skipped** — quest card 4 (6794, `calloway_fucked_once`) already IS the "He's yours" card. Live-verified: rungs present→gone (not greyed), prose flips, drain loop persists. *(Ladder-timing nit noted for later: card 4 is gated on first-sex, not the drain, and its text assumes the drain.)*

Original change-table (for reference):

**Current state (verified line numbers, 5_scenes.toml):**

| Canvas / choice | Line | Now | Target after `calloway_drains_done gte 1` |
|---|---|---|---|
| `hub_calloway_fileroom` base | 5344 | Opener reads "testing, earning" | Register flips to *owned*. The opener stays ONE constant paragraph (lanes.md:136-140); the change lives in the choices below. |
| "Talk to him." choice → `.talk` (+2 relation) | 5371 | Trust-building "walk me through the ghost", +2 relation | **Swap or retire.** She's not building trust — she has it. Either close it (`calloway_drains_done lt 1`) or swap to a short possessive owner's check-in. |
| "Get close to him." → `rung_calloway_contact` | 5382 | Seduction rung, still selectable | **Close** on `calloway_drains_done lt 1` — past seducing him. |
| "Take him in your mouth." → `rung_calloway_oral` | 5397 | Seduction rung, still selectable | **Close** on `calloway_drains_done lt 1`. |
| "Take him — all the way." → `loop_calloway_sex` | 5418 | Full-sex loop entry (→ finisher → drain) | **KEEP.** This is the drain loop; the warm-tap repeat is intended. |
| `work_the_case` "earn his belief" grind | 5472 | +3 relation, courtship framing, repeatable | **Reframe the body** via `[group]` (it's a drain-activity, not a hub opener, so `[group]` is allowed): drop "earn his belief"; it's just cover-work now. |
| `loop_calloway_finisher` d0/done swap | 6149 | "Open the drain on him." (6194, first) → "Take him again." (6211, repeat) | **Already correct** — the intra-loop swap reacts to `calloway_drains_done`. No change. |

**Mechanism notes:**
- Closing a hub choice = add `conditions {calloway_drains_done lt 1}` with **no** `show_when_locked` → it hides once the drain fires (do NOT add `show_when_locked` on this consumed gate — that's the stale-locked_text trap).
- A possessive successor verb (optional) = a new hub choice gated `calloway_drains_done gte 1` that replaces the retired seduction verbs.
- `work_the_case` body swap = two `[group]` blocks: group[0] `{calloway_drains_done lt 1}` (current "earn his belief"), group[1] `{calloway_drains_done gte 1}` (post-ownership cover-work).

**Also (small, optional):** the Calloway quest ladder (5_scenes.toml ~6755-6795) ends at card 4 "Break him all the way open" (gated `calloway_fucked_once`). There is no post-drain "he's yours / owned" card — the ownership flip is written only there. Consider a 5th card on `calloway_drains_done gte 1`.

---

## 6. Complete change inventory (reference)

**Already correct — do NOT touch (avoid over-fixing):**
- **Vane:** `walkin_chat_vane` drops on `vane_confirmed`; `cap_docs_vane_routine` self-gates `vane_confirmed is_false + docs_retrieved is_false`; blackmail one-shot. All shut post-beat. *Residual (cosmetic, low priority):* his `[[npcs.schedules]]` is unconditional, so he still reads "present" after he flees — but he has no portrait hub and every canvas is gated shut, so nothing is interactive. Post-blowup the whole docs floor seals anyway, making it moot.
- **One-shots that self-retire:** `cap_archive_cover`, `cap_calloway_meet`, `cap_calloway_access`, `cap_calloway_flinch`, `cap_case_insider/curated/pipe`, `cap_first_penthouse_service`, `salvage_mercer_shocked`, `cap_1a_close`.

**Dead labels found (housekeeping, not blocking):**
- Calloway `arc_stages` declares "Betrayed" (1_metadata) but nothing ever sets it → a label, not a live gate.
- `authoring_state.json` `npc_vane` entry still describes the stale pre-v2 "theft #1/#2 / unseen hand" design, contradicted by the shipped on-screen-blackmail recast. Ledger out of sync with the built TOML.

---

## 7. Skill / doctrine fix — **DONE** (author-game, 2026-07-23, uncommitted)

**Shipped:** a new named subsection **"Retire the standing surface on the terminal flag"** in `references/lanes.md` (right after Lane 4) — the terminal beat's setter flag is the audit key: sweep the NPC's whole standing cluster (hub choices · Lane-2 ambients · Lane-3 walk-in/drain/work · schedule presence · floor) and gate each on it, via a per-canvas gate/`[group]`-swap **or** the zone-seal chokepoint shortcut; reconciled with the presence-floor rule (leave a quiet in-character hub; retire only a *contradictory* surface). Surfaced via a per-beat **doctrine self-audit** bullet in `references/beat-authoring.md` (next to `frontier`) + a §4E back-pointer in `references/content-framework.md`. Logged in the author-game `CHANGELOG.md`. **No lint** (a clean one is infeasible — it false-positives on the zone-seal pattern the doctrine recommends) and **no subagent eval** (this session's cascade eval was non-discriminating; verified directly against the Calloway/Mercer case instead — the doctrine names exactly the surfaces missed + both mechanisms used).

Original spec (for reference):

The systematic gap (§1). Add to `author-game`:

1. **A named pattern** — "retire the standing surface on the terminal flag." When a one-way TERMINAL beat fires, audit **every** surface the NPC still offers — Lane-1 hub, walk-in bucket, ambient pool, drain/work activity, schedule presence, and the surrounding floor cluster — and gate each on the terminal flag to close or swap it. Home: content-framework.md §4E (post-capstone checklist) and/or lanes.md near the self-retiring-capstone doctrine (lanes.md:293). Distinguish it from the capstone self-retire (which only covers one-shots).
2. **Note the zone-seal shortcut** — when an NPC/interaction cluster lives on one location tree reachable through a single chokepoint (a travel gate, a locked entry), sealing the chokepoint retires the whole cluster in one move (cheaper and un-leakable vs. per-canvas edits). This is the Phase-2 pattern; it's reusable.
3. **Consider a lint** (stretch) — flag an NPC that has a terminal one-shot capstone setting a flag whose fiction implies departure/blown-cover, while their standing hub/work/floor canvases carry no guard on that flag. Hard to detect fully (fiction-implies-departure isn't machine-readable), so a §4E checklist item is the realistic backstop; a lint is optional.
4. **CHANGELOG.md** — log any skill edit in the same turn (skill-ledger rule).

**Test:** "Would a correct author-game skill have prevented the Calloway floor?" → Yes. So the fix ships in the skill, not just Vesper.

---

## 8. Open decisions (pending LO)

1. **Drain-again lifetime.** Currently keyed to the blowup: the warm-tap repeat (`loop_calloway_finisher` "Take him again") survives the undercover window and disappears when the Spire seals. Alternative: make the drain strictly one-and-done (cut the repeat entirely). **Default in place = keyed to blowup.**
2. **"Talk to him" post-drain** — close it, or swap to a possessive check-in? (§5)
3. **Post-drain quest card** — add a 5th "he's yours" Calloway card, or leave the ladder ending at card 4? (§5)
4. **Skill-fix scope** — doctrine + checklist only, or also attempt the lint? (§7)

---

## 9. Build & verify procedure

```
cd story_gen_django && source venv/bin/activate
python scripts/merge_toml_phases.py games/vesper --validate
python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \
  --output games/vesper/output --video-folder games/vesper/videos --dev --debug
```
Green gates required: `validation: OK` (merge) + `✓ Validation passed` + `✓ All flag chains valid` (package).
The Archive is test-portal only (never publicly shipped; releases stop at v0.1.3), so `--dev --debug` is the intended mode.
Live test: serve `games/vesper/output` on a port; Playwright + `window.SugarCube.State.variables.flags.<k>` + `Engine.play("Canvas_<id>_Node_<node>")`.

---

## 10. Status ledger

| Rev | What | State |
|---|---|---|
| 84 | Calloway WHERE re-gate (drain names the vault) | uncommitted |
| 85 | Colm hub rebuild | uncommitted |
| 86 | Cascade layout fix + skill cascade doctrine | uncommitted |
| 87 | Phase 2 — the Spire seal (this doc §4) | uncommitted |
| 88 | Phase 1 — Calloway "he's yours" swaps (§5) | uncommitted |
| skill | Skill/doctrine fix — author-game "retire the standing surface" (§7) | uncommitted (author-game CHANGELOG 2026-07-23) |

**Nothing committed.** Revs 84–88 + the author-game skill edits are stacked, awaiting LO's "commit and push."
