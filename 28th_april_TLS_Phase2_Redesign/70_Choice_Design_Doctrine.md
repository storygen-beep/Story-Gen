# Doc 70 — Choice Design Doctrine

**Date:** 2026-05-27 (revised same day to add flag-provenance trace + phone-system cross-refs)
**Status:** Active doctrine
**Sibling docs (click-design):** Doc 24 (3 Lanes), Doc 50 (Quest Card Shape), Doc 56 (RTS Principles + Alignment), Doc 57 (Capstones)
**Sibling docs (phone-system architecture):** Doc 42 (RTS Phone Reference), Doc 43 (Engine Phone As-Built), Doc 44 (Parity Gap PRD), Doc 45 (100% Parity PRD — shipped), Doc 46 (TLS Phone Design — shipped). Doc 70 is the **click-design lens** applied on top of this architecture; it does NOT re-document the phone system itself.
**Scope:** Click-level rule. When does a click expand into 2+ options vs. a single advance? What makes a fork mechanically real vs. decorative? Applies to ALL click affordances (hub menus, cascade beats, exit blocks, phone reply arrays), not just phone.

---

## §1 — Why this doc exists

A 2026-05-27 audit of TLS phone reply choices surfaced a pattern-level defect that isn't local to the phone: choices are being authored as if every click should fork, when the underlying RTS reference uses click-to-advance as the dominant pattern and reserves forks for state-routed consequences.

The forensic numbers, verified against `game_explorations/road-to-success/passage_catalog.json` and `games/the_long_summer_test/toml_phases/7_final_game.toml`:

**RTS (361 passages):**
- 1559 `<<linkreplace>>` macros (sequential cascade beats — click IS the advance)
- 94 real `<<if>>`-gated forks
- **6% fork-to-beat ratio**
- 6 cross-passage `<<link>>` macros total — essentially unused
- Quest-bus macros: 25 `<<StartQuest>>`, 30 `<<UpdateQuest>>`, 29 `<<FinishQuest>>`, 9 `<<UnlockLocation>>`, 16 `<<NotifyPhone>>`

**TLS (`7_final_game.toml`, 83 canvases):**
- 166 hub menu items (`[[canvases.nodes.exit_block.choices]]`) across 38 canvases — RTS-faithful tier-gated rungs
- 52 cascade `advance_text` taps inside 43 cascades — RTS-faithful click-advance reveal
- 9 inline `choices = [...]` blocks, **all 2-option, all in phone conversations**

**TLS phone fork audit:** 6 phone-set flags total. **5 of 6 have zero downstream consumers in the slice.** The choice presented to the player is mechanically inert — the flag fork doesn't gate anything, and the trait deltas land at stages where the relevant gates have already been passed. §4.3 below traces each flag's history through prior doctrine docs — three of the dead flags are doctrine-contradiction (retired by Doc 19, flagged for removal by Doc 20, then re-introduced by Doc 46), two are Phase 2+ seeds (Doc 58 intent), one is ambiguous.

The prompts_v2/ folder (Doc 66, held) will generate dozens of games. Without a doctrine document on when a click should be a fork vs. an advance, every generated game will reproduce this pattern: choice-shaped UI that pretends to branch but doesn't route content. Doc 70 fills that gap.

### §1.1 — Scope boundary vs. phone-system architecture docs

The phone system itself is documented elsewhere. **Doc 70 does NOT re-document phone-system architecture** — it applies the click-design lens to phone affordances among other surfaces. If you're authoring a phone-bearing game, read in this order:

1. **Doc 42** — what RTS's phone actually does (8 subsystems, dispatch bus, hardware-gate doctrine, daily cadence).
2. **Doc 43** — what the engine already supports today (`v2.py:1494–2166` runtime block).
3. **Doc 45** — the parity gaps that have been shipped (G1–G12 all closed: notifications, social posting, photo actions, real quest primitive, delay queue, corruption tiers, gallery, custom apps, fast jobs, bank, in-world purchase).
4. **Doc 46** — TLS's specific implementation (9 conversations + 3 daily topics + 5 photo actions, chat-centric subset).
5. **Doc 70** — THIS doc — applies T1–T5 to every clickable affordance inside the phone (and outside it).

A phone built without Doc 70's click-design rules will have the dead-flag-fork defect this doc audits. A phone built without Docs 42-46 won't exist at all.

---

## §2 — RTS choice pattern map (evidence-backed)

Four categories cover every clickable affordance in RTS. Counts are verified against the passage catalog.

| Category | Macro | Count | Role |
|---|---|---:|---|
| **Cascade beat** | `<<linkreplace>>` | 1559 | Sequential reveal inside a scene — click IS the advance, text describes what just happened |
| **Hub tier rung** | `<<button>>` + `<<if>>` gate | 696 buttons / 814 if-gates | Location hubs (Bedroom, City, Beach) — tier-gated menu items |
| **State-routed fork** | `<<if getCorruptionLevel() >= N>>`, `<<if $clothes.X.purchased>>` | 94 | Single binary fork inside a scene, reads existing accumulated state |
| **Chat-with-consequence** | `<<InvitationMessage>>` widget, `<<linkreplace>>` containing `<<StartQuest>>` / `<<UpdateQuest>>` / `<<UnlockLocation>>` | (encapsulated in `InstafameMessages`, `PhoneMessages`) | Reply persists to `$player.phone.messageStates[key]`, triggers quest bus or location unlock |

### §2.1 — Worked example: scene cascade (the 94% case)

`SellingMyStepsister` — passage with 18 `<<linkreplace>>` and 1 `<<if>>` fork. Top-level structure:

```sugarcube
<<Speech Brother "I need an answer now. He's waiting.">>

<div id="acceptSelling">
<<if getCorruptionLevel() >= 3>>
<<linkreplace "Accept">>
    <<HideDiv "refuseSelling">>
    <h3>You accept your $npc.Brother.relationship's offer...</h3>
    <<video 'house/bedroom/sellingMyStepsister/sellingMyStepsister3'>>
    ...
<<linkreplace "He arrives">>
    <h3>A few minutes later, your $npc.Brother.relationship's friend arrives.</h3>
    ...
<<linkreplace "You sit down">>
    ...
<<linkreplace "He gives you the money">>
    <<AddMoney 500>>
    ...
```

**One fork at the top** (corruption ≥ 3 → Accept branch unlocked, else Refuse only). Inside the chosen branch, **17 sequential `<<linkreplace>>` beats** — each click advances one beat, the click text describes what just happened ("He arrives", "You sit down", "He gives you the money"). The player isn't picking a personality at every click. They're tapping forward.

### §2.2 — Worked example: chat-with-consequence (the 6% case, done right)

`VeronicaCostumePartyMessage` widget in `PhoneMessages`:

```sugarcube
<<widget "VeronicaCostumePartyMessage">>
    <<set _stateKey = _args[0] || "VeronicaCostumeParty">>
    <<InvitationMessage _stateKey "Veronica" "Hey, I'm organizing a costume party..." "I'll be there, Veronica." "I'm sorry, Veronica, but I can't go.">>
    <<if $player.phone.messageStates[_stateKey] is undefined>>
        <div class="phone-invitation-actions">
            <<link "Accept the invitation">>
                <<set $player.phone.messageStates[_stateKey] = "accepted">>
                <<if $clothes.costume1.purchased>>
                    <<UpdateQuest CostumeParty 2 "I should go to Veronica's house on Saturday in my fairy costume">>
                <<else>>
                    <<UpdateQuest CostumeParty 1 "I should buy a fairy costume for the party at the mall">>
                <</if>>
                <<NotifyPhone "The quest Costume Party has been updated!">>
                <<RefreshMessages>>
            <</link>>
            <<link "I can't go">>
                <<set $player.phone.messageStates[_stateKey] = "declined">>
                <<RefreshMessages>>
            <</link>>
        </div>
    <</if>>
<</widget>>
```

Every consequence-bearing path is exercised:
- **Accept** → persists `messageStates["VeronicaCostumeParty"] = "accepted"`, updates an active quest objective, branches the objective text on inventory (`$clothes.costume1.purchased`), pushes a phone notification.
- **Decline** → persists `messageStates["VeronicaCostumeParty"] = "declined"`, quest path closes.
- **Re-visit later** → `<<if $player.phone.messageStates[_stateKey] == "accepted">>` (in `InvitationMessage`) reads the persisted state and renders the accept-confirmation prose.

Similarly, `<<JimDM>>` in `InstafameDM`:

```sugarcube
<<if getCorruptionLevel() >= 4>>
    <<linkreplace "Accept the proposal">>
        <<NotifyPhone "Jim's Studio is now unlocked on the city map">>
        <<UpdateQuest Pornstar 1 "I should visit Jim's studio">>
        <<UnlockLocation filmStudio>>
    <</linkreplace>>
<<else>>
    <<linkreplace "I can't do this">>
        <<NotifyCorruption 4>>
    <</linkreplace>>
<</if>>
```

The Accept branch **unlocks a navigable map location** the Decline branch doesn't reach. Refusal pays out 4 corruption (`<<NotifyCorruption 4>>`) so the symmetric outcome lands the player in a different downstream corruption band.

---

## §3 — RTS choice rules, derived (R1–R5)

The doctrine extracted from the evidence in §2:

### R1 — Click ≠ decision

Default click semantics = advance the scene. Decisions are state-gated branches, not personality votes.

**Why:** 94% of RTS clicks are sequential cascade beats. The click moves the camera forward; the text describes what's happening. The player isn't being asked to characterize themselves — they're being shown the next beat.

**How to apply:** When writing a click affordance, ask whether it ADVANCES the same scene or BRANCHES to a different outcome. If advance → single `<<linkreplace>>` (RTS) / single exit advance (TLS). If branch → check R2–R5.

### R2 — Forks are state-routed, not flag-introduced

RTS reads accumulated state (corruption tier, beauty band, inventory ownership, quest progress, time of day) to pick which branch to render. The fork doesn't introduce a new flag — it READS one.

**Why:** Forks that introduce new flags multiply the state space. Forks that read existing state collapse the state space into already-tracked tiers (RTS has ~5 macro-stats; everything routes off them). Authoring complexity stays bounded.

**How to apply:** Before adding `flagEffects` to a choice, ask whether the same routing could be done by reading an existing trait band (corruption, beauty, love, trust, stage). If yes, use the trait band and skip the new flag. New flags are reserved for capstone-shape forks (Doc 57) where both paths get scripted scenes downstream.

### R3 — Persisted state must be consumed

If a click sets `messageStates[key]`, an `unlocks_X` flag, or any `_route_*` flag, some later passage MUST read it. Setting state that nothing reads = lie about agency.

**Why:** The TLS audit found 5 of 6 phone-set flags have zero readers. The player makes a choice that visibly looks like a fork; the engine writes a flag; nothing in the game ever reads the flag again. The choice is theater.

**How to apply:** Before shipping a choice with `flagEffects`, grep the rest of the slice for the flag name. If zero hits outside the setter — either author the consumer in the same change (Option A in §6) or remove the `flagEffects` (Option B). Cite the consumer's file:line in the canvas comment.

### R4 — Hub menu = tier-gated rungs

Hub menu items are tier-gated rungs. Each item is `<<if>>`-gated visible-when-locked or hidden, gated by a stat threshold the player either has or doesn't. The player picks a rung they've earned — not voting on a personality.

**Why:** Hubs are the engine's primary surface for "what can I do here right now." They are NOT moments of dramatic forking. The dramatic fork is what gets the player TO a new tier; the hub just exposes what that tier unlocks.

**How to apply:** Every menu item in `[[canvases.nodes.exit_block.choices]]` should have either `show_when_locked = true` + `conditions` block OR `conditions` block + hide-when-failed. Always-shown, always-clickable menu items violate R4. The Frank kitchen morning hub is the reference implementation (`7_final_game.toml` ≈ L2700): Tease (corr ≥ 5), Flash (corr ≥ 15), Suck (corr ≥ 25), Have sex (corr ≥ 25).

### R5 — No flavor-fork

If a click has only one consequence-bearing outcome, use a single `<<linkreplace>>` (or single TLS exit advance). Don't manufacture 2 options when only 1 routes content.

**Why:** Flavor-forks (2 options that BOTH grant a small trait delta but route nothing) train the player to ignore choice. After the third decorative fork, every fork looks decorative. Real forks lose their weight.

**How to apply:** When tempted to give the player a "personality" choice (warm vs. cold reply, kind vs. cynical thought), ask whether either branch will be observable in any later content. If no — collapse to one advance. The trait delta still happens; the click is honest about what it does.

---

## §4 — TLS current state (audit table)

### §4.1 — Works (RTS-faithful)

| TLS pattern | Count | Equivalent RTS pattern | Verdict |
|---|---:|---|---|
| Hub `exit_block.choices` rungs | 166 / 38 canvases | `<<button>>` + `<<if>>` gate | ✓ Works — tier-gated, stage-aware (Frank kitchen/dinner/livingroom/yard hubs, Marge diner hub) |
| Cascade `advance_text` taps | 52 / 43 cascades | `<<linkreplace>>` sequential reveal | ✓ Works — click-advance reveal pattern (loop_franks_bedroom_sex, all per-NPC scenes) |

### §4.2 — Broken (anti-pattern), split by provenance

All 9 inline `choices = [...]` blocks live in phone conversations. Six set flags. Naive zero-reader audit calls 5/6 "dead." Tracing each flag's history through prior doctrine docs reveals **three distinct failure modes**, each with a different remediation. §4.3 walks the trace; the table here summarizes the verdicts.

| Phone conversation | Flag(s) set | Category | Doctrine status | Verdict |
|---|---|---|---|---|
| `frank_after_catch` | `frank_terms_accepted`, `frank_keep_route_rupture` | Mixed (Cᴬ + Cᴿ) | `_terms_accepted` ambiguous (Doc 46 introduced, no consumer specified); `_rupture` retired by Doc 19, flagged for removal by Doc 20 | ✗ Partial doctrine-contradiction |
| `frank_sleepover` | `frank_keep_route_romantic`, `frank_keep_route_arrangement` | Cᴿ (Retired) | Both retired by Doc 19, flagged for removal by Doc 20, re-introduced by Doc 46 against doctrine | ✗ Doctrine-contradiction (re-resurrected dead flags) |
| `ryan_partner` | `ryan_keep_route_yes_engaged`, `ryan_keep_route_not_yet` | Cˢ (Seed) | Doc 58 explicitly declares these as "Phase 2+ branch outcomes" — intentional seeds, consumers not yet authored | ⚠ Seeded — pending Phase 2+ |
| `anon_1` | `anon_dm_seen` | n/a | Set by `anon_1`, read at L1382 by `anon_2.trigger.conditions` | ✓ Correctly built |

Verification commands used:
```bash
grep -nE "flag = \"<flag>\".*op = \"set\"" 7_final_game.toml   # setter count
grep -nE "flag_key = \"<flag>\"" 7_final_game.toml             # reader count
grep -rE "<flag>" 28th_april_TLS_Phase2_Redesign/              # prior-doctrine provenance
```

**Category legend:**
- **Cᴬ — Ambiguous.** Introduced without explicit consumer spec; no prior doctrine retiring or seeding it. Requires LO call: seed for Phase 2+ or remove.
- **Cᴿ — Retired.** Prior doctrine explicitly dropped the flag; re-introduction violates that decision. Remove.
- **Cˢ — Seed.** Prior doctrine explicitly declares the flag as Phase 2+ intent. Either author consumers (T3 wire-it) or formally defer with a slice-comment.

### §4.3 — Flag provenance trace (per flag)

For each phone-set flag, the trace through doctrine history. Cite paths so future readers can verify.

#### Frank `keep_route_*` (4 flags: `_romantic`, `_arrangement`, `_rupture`, `_power_inverted`) — Category Cᴿ

- **Doc 02 — `02_NPC_Stage_Chains.md`** originally designed `frank_keep_route in {romantic, arrangement, rupture, power_inverted}` as the Stage 4 routing surface. Per-route scene branches in bedroom + office were planned.
- **Doc 19 — `19_Frank_Stage_3_Plus_Design.md`** EXPLICITLY DROPPED the design: *"Doc 02's `frank_keep_route in {romantic, arrangement, rupture, power_inverted}` design is dropped... One `frank_stage_4` helper. No `frank_keep_route_*` flags."*
- **Doc 20 — `20_Frank_Slice_RTS_Doctrine_Review.md`** flagged the orphaned declarations: *"Dead flag declarations. `frank_keep_route_romantic` / `_arrangement` / `_rupture` / `_power_inverted` still in flag_keys list even though doc 19 §1 explicitly drops the 4-keep-route design. Remove during next maintenance pass."*
- **Doc 46 — `46_TLS_Phone_Design.md`** then RE-USED them in chat reply choices, framing them as *"the slice's existing `frank_keep_route_*` seed flags rather than inventing new endings"* — without acknowledging Docs 19/20 had retired them.

**Diagnosis:** These flags are NOT seeds. They were retired and queued for removal. Doc 46 mis-read the orphaned declarations as intentional. Doc 70 §6.1.1 prescribes removal per Doc 20.

#### Ryan `keep_route_*` (3 flags: `_yes_engaged`, `_not_yet`, `_no_withdrawn`) — Category Cˢ

- **Doc 58 — `58_Ryan_Design_Brief.md`** explicitly declares: *"`ryan_keep_route_*` — 3 variant flags for Phase 2+ branch outcomes."*
- No prior doctrine retires them.

**Diagnosis:** These are intentional Phase 2+ seeds. The Phase 2+ consumers haven't been authored yet because Phase 2+ itself is held (Doc 65). Doc 70 §6.1.2 prescribes a per-flag LO call: wire-now, collapse, or formally defer with slice-comment.

#### `frank_terms_accepted` (1 flag) — Category Cᴬ

- **Doc 46 — `46_TLS_Phone_Design.md`** introduced this flag for the `frank_after_catch` Accept choice. Doc 46 does NOT name a downstream consumer.
- No prior doctrine retires or seeds it.

**Diagnosis:** Ambiguous. Could be Phase 2+ seed (intended but undocumented) or drift (the chat-design author wanted "feels-like-a-choice" weight without authoring consumers). Doc 70 §6.1.3 prescribes an LO call.

The five trait-only phone forks (no `flagEffects`, only trait deltas):

| Phone conversation | Trait deltas | Downstream effect | Verdict |
|---|---|---|---|
| `frank_after_office` | +2 love OR +2 corruption | No active gate at the relevant stage | ⚠ Soft anti-pattern |
| `jake_sorry` | +3 trust OR (+2 corr, +1 corr) | No active gate at Stage 1 | ⚠ Soft anti-pattern |
| `jake_tease` | (+1 arousal, +1 corr) OR +2 trust | No active gate | ⚠ Soft anti-pattern |
| `ryan_thanks` | +3 trust OR +3 love | +3 trust would feed Stage 0→1 (`trust >= 10`) but chat fires AT Stage 2 | ⚠ Soft anti-pattern (timing-misaligned) |
| `anon_2` | (+3 corruption) OR (+1 calculation) | No active gate; `calculation` declared but unused at slice scale | ⚠ Soft anti-pattern |

The trait deltas DO route relationship state in principle, but the chat thread triggers (`ryan_partner_open`, `frank_caught`, `jake_peek_draw_revealed`) all fire AFTER the trait-driven Stage advance that would consume those deltas. The +N stat lands in a state band that nothing currently gates on.

---

## §5 — The 5-rule decision test (T1–T5)

A click should expand into 2+ options ONLY if at least one of T1–T5 is true. This is the load-bearing core of the doc — cite as **Doc 70 T1** through **Doc 70 T5** in canvas comments.

### T1 — Quest line opens/closes

Accept starts a `quest_card` (Doc 50); Decline closes that path. Both branches are observable in subsequent slice content.

**RTS reference:** `<<InvitationMessage>>` widget → `<<StartQuest PoolParty>>` on Accept; "no problem maybe next time" on Decline. The accepted-state is read on the future Saturday passage; the declined-state means that party never happens.

**TLS form:** Accept choice → `flagEffects = [{ flag = "X_quest_open", op = "set" }]` + a `quest_card` whose `trigger` reads `X_quest_open`. Decline → no flag, no card. Card never appears.

### T2 — Location/canvas unlocked or locked

One branch makes a future canvas reachable that the other branch doesn't.

**RTS reference:** `<<UnlockLocation filmStudio>>` inside the Accept branch of `<<JimDM>>`. After Accept, the city map exposes the studio; after Decline, it doesn't.

**TLS form:** Accept choice → `flagEffects` sets a flag that a future canvas's `conditions` block requires. Without the flag, the canvas can't fire — the location is effectively locked. The slice has no canvas-level lock primitive yet, but a `trigger.conditions` flag check IS the lock.

### T3 — Subsequent text branches

A later passage or conversation reads the persisted state and renders different prose.

**RTS reference:** `<<if $player.phone.messageStates[_stateKey] == "accepted">>` inside `<<InvitationMessage>>` renders the post-accept dialog; the same block renders the post-decline apology if `== "declined"`. The same widget body reads the persisted choice on every re-visit.

**TLS form:** A future canvas's body block uses a conditional cascade or substitution rule that reads the route flag. Romantic-Frank ambient (`frank_keep_route_romantic == true`) renders different prose than arrangement-Frank ambient (`frank_keep_route_arrangement == true`).

### T4 — Tier-gated hub rung

The player picks a tier they've earned (corruption / beauty / love / stage). State is the gate, not the result.

**RTS reference:** Bedroom hub — `<<if getCorruptionLevel() >= 2>>` reveals the masturbation rung; `<<if $player.relationships.brother.corruption >= 3>>` reveals the brother-incest rung. Each rung visible-when-locked or hidden.

**TLS form:** `[[canvases.nodes.exit_block.choices]]` with `show_when_locked = true` + `conditions` block. Frank kitchen morning hub at `7_final_game.toml` ≈ L2700 is the reference. T4 forks DO have multiple visible options at once, but every option's visibility is state-gated.

### T5 — Doctrinal threshold crossed

RTS-style stat-payout: refusing pays +N to a different stat axis so the symmetric outcome reads downstream as a different stat band.

**RTS reference:** `<<NotifyCorruption 4>>` on the Decline branch of `<<JimDM>>`. Refusing the porn proposal still moves the player's corruption needle (the moment imprinted), and the +4 corruption may push them past the next band threshold (≥ 5, ≥ 10) that other content gates on.

**TLS form:** Two options, each granting +N to a DIFFERENT stat axis whose downstream band actually gates content. ryan_partner Yes (+4 love) vs Not yet (+2 trust) WOULD be T5-compliant IF the slice had a downstream Ryan canvas gated on love-band-3 vs trust-band-2. As authored, neither band has a consumer at the post-Stage-2 timing.

### If none of T1–T5 are true

**Collapse the fork to a single advance.** The click is then honest:
- The trait delta still fires (single-choice can still have `effects`).
- The player isn't being shown two paths that lead to the same place.
- Authoring budget is freed for forks that DO route content.

Cite **Doc 70 R5** in the canvas comment when collapsing.

---

## §6 — Concrete remediation menu for current slice

Three options per dead-flag fork. The doc lays out moves; LO picks per-fork.

### §6.1 — Per-category remediation (post §4.3 trace)

The naive "dead = pick A/B/C" framing collapses three different problems into one menu. After the §4.3 provenance trace, each category has its own appropriate move.

#### §6.1.1 — Category Cᴿ (Retired) — Frank `keep_route_*` flags

**Prescription: remove.** Doc 20 already specified this; the chat threads in Doc 46 re-introduced the flags against doctrine. Specifically:

- In `frank_after_catch`: remove `flagEffects` entry setting `frank_keep_route_rupture`. Keep the trait delta (Frank trust −3). Keep the `frank_terms_accepted` entry on the Accept branch pending the §6.1.3 decision.
- In `frank_sleepover`: remove BOTH `flagEffects` entries (`frank_keep_route_romantic` + `frank_keep_route_arrangement`). Keep trait deltas (Frank love +3 OR trust +2).
- Remove the four declarations from the `flag_keys` list (`7_final_game.toml` L305-308): `frank_keep_route_romantic`, `frank_keep_route_arrangement`, `frank_keep_route_rupture`, `frank_keep_route_power_inverted`.
- Doc 46's framing ("re-use existing seed flags") needs a one-line correction noting Docs 19/20 retired them.

The Frank chat choices then become R5-compliant trait-only forks (love-leaning vs. trust-leaning), which §6.2 addresses on whether to collapse further.

**No LO call needed — Doc 20 already made it. This is mechanical cleanup.**

#### §6.1.2 — Category Cˢ (Seed) — Ryan `keep_route_*` flags

**LO call locked 2026-05-27: option (C) Formally defer with seed-comment.** Executed in `7_final_game.toml` at the declaration block + the `ryan_partner` choice block — both carry inline comments citing Doc 58 + naming the intended Phase 2+ consumer (engaged Ryan → faster Stage 3 / different ambient register; not-yet Ryan → more trust before E8). To re-evaluate when Phase 2+ resumes per Doc 65. Original three-option menu retained below for future reference.

**Three honest options:**

- **(A) Wire it NOW.** Author the Phase 2+ consumers Doc 58 always intended. Engaged Ryan (`_yes_engaged is_true`) gets faster Stage 3 access / different prose at later capstones; Not-yet Ryan (`_not_yet is_true`) needs more trust accumulation before E8 fires; Withdrawn Ryan (`_no_withdrawn`) sees the arc close. Becomes T1/T3-compliant.
  - **Cost:** authoring Phase 2+ Ryan content NOW, which means crossing the Doc 65 Phase 2+ hold line.
- **(B) Collapse for the slice.** Strip the `flagEffects`, keep trait deltas, remove flag declarations. The ryan_partner chat becomes a +4 love OR +2 trust nudge with no fork-flag. When Phase 2+ authoring resumes, re-introduce the flags then.
  - **Cost:** delete-and-defer; trivial.
- **(C) Formally defer with seed-comment.** Keep the `flagEffects` AND keep the flag declarations, but add an inline TOML comment naming the Phase 2+ consumer that will read them. Comment cites Doc 58. Slice-clean; visible to future authors.
  - **Cost:** ~3 lines of comment per choice.

**Recommended default: (C).** Doc 58 already declared these as Phase 2+ seeds. Removing them now (option B) just creates re-work when Phase 2+ resumes. Wiring now (option A) violates Doc 65's hold. Formal defer with seed-comment is the doctrinally honest move.

#### §6.1.3 — Category Cᴬ (Ambiguous) — `frank_terms_accepted` flag

**LO call locked 2026-05-27: Phase 2+ seed — keep with seed-comment (treat as §6.1.2 (C)).** Executed in `7_final_game.toml` at the declaration (L343-area) + the `frank_after_catch` choice block — both carry inline comments citing the intended Phase 2+ consumer (Frank "arrangement-accepted" route: different morning-after register, different bedroom hub openings, possible Stage 4 routing variant). To re-evaluate when Phase 2+ resumes per Doc 65. Original ambiguity framing retained below for future reference.

**Options that were on the table:**

- If Phase 2+ seed: keep the `flagEffects`, add seed-comment naming the Phase 2+ consumer that will read it (treat as §6.1.2 (C)).
- If drift: remove the `flagEffects`, remove the flag declaration from `7_final_game.toml` L341 area, collapse to trait-only fork.

Doc 46 §3 introduced this flag for the Frank "arrangement accepted" route but doesn't name a consumer. The flag's name suggests Phase 2+ intent (a "terms-accepted" Frank arc would route differently than a "haven't agreed" Frank), but the intent isn't recorded anywhere in the doctrine docs.

**LO call surface:** "Was `frank_terms_accepted` ever supposed to do something downstream?" If yes → seed-comment per §6.1.2 (C). If no → remove per §6.1.1.

#### §6.1.4 — Reference implementation (unchanged)

`anon_dm_seen` is the one TLS phone fork that satisfies T3. Model future phone forks on it:
- `anon_1` Accept choice → `flagEffects = [{ flag = "anon_dm_seen", op = "set" }]`
- `anon_2.trigger.conditions` → `{ type = "flag", flag_key = "anon_dm_seen", operator = "is_true" }`

The flag set on the first chat is the gate that opens the escalation chat. Player agency is preserved across the chain. The same shape (set-in-chat-A, read-in-chat-B) is what §6.1.2 (A) "wire it now" would produce for Ryan's keep-route flags if LO chooses that path.

### §6.2 — Trait-only forks (5 phone fork pairs)

For each of `frank_after_office`, `jake_sorry`, `jake_tease`, `ryan_thanks`, `anon_2`: these have NO `flagEffects` (only trait deltas), so the §6.1.1/§6.1.2/§6.1.3 category split doesn't apply. The fork still fails T1–T5 because the chat threads fire AFTER the relevant Stage-transition trait gates — the +N stat lands in a band nothing currently gates on.

**Prescription: collapse (R5) by default.** Strip each choice array to a single `linkreplace` / single exit advance with one trait delta. The chat still happens; the player still gets a stat bump; there's no fake fork.

Exception: if LO wants to author downstream content that gates on the trait band these deltas push the player into (e.g. a "Frank love ≥ 8" canvas, a "Jake corruption ≥ 5" peek-draw revelation), then keep the fork — but author the gate-bearing canvas in the same change. Otherwise the trait delta is decoration.

`ryan_thanks` is the most defensible to keep as a fork (+3 trust vs +3 love) because if Stage 0→1 retroactively becomes love-gated instead of trust-gated, the +3 love branch would route. But that gate doesn't exist today; it's hypothetical.

---

## §7 — Pre-authoring checklist

Use BEFORE writing any choice array or multi-option exit block. Five questions, each mapped to one T-rule. If all five are No, no fork.

- [ ] **T1 — Does the click open or close a `quest_card`?** Name the card. Cite the `[[quest_cards]]` entry that will consume the flag.
- [ ] **T2 — Does it unlock or lock a canvas/location?** Name the future canvas. Cite the `trigger.conditions` block that will read the flag.
- [ ] **T3 — Does some later passage check this flag/state?** Cite the file:line of the consumer (a `conditions` block, a `[group]` predicate, a substitution-rule condition).
- [ ] **T4 — Is this a tier-gated hub rung where state is the gate?** Confirm the menu item has `show_when_locked = true` + `conditions` block; the state ALREADY exists (corruption tier, love band, etc.) and isn't being introduced here.
- [ ] **T5 — Does the symmetric outcome land in different downstream bands?** Confirm Branch A's stat delta (+N to stat X) and Branch B's stat delta (+M to stat Y) push the player across band thresholds that downstream content gates on. Name the thresholds.

**If all five are No:** collapse to a single advance. Cite **Doc 70 R5** in the canvas comment so the reviewer knows the collapse was intentional, not an oversight.

---

## §8 — Sibling-doc cross-refs

### §8.1 — Click-design siblings (Doc 70 R1–R5 / T1–T5 derive from these)

- **Doc 24 (3 Lanes)** — Lane 1 hub buttons follow R4 (tier-gated rungs). Lane 2/3 substitutions and ambients follow R1 (click-advance default; cascade beats). Lane 4 capstones are where T1/T3 forks live with scripted consequence-chains.
- **Doc 50 (Quest Card Shape)** — quest cards opened/closed by T1 forks. Card shape (R1-R6 in Doc 50) is unchanged; the click that gates a card's appearance follows Doc 70.
- **Doc 56 (RTS Principles + Alignment)** — Doc 70 R1–R5 derive from RTS evidence and are consistent with P1–P10 in Doc 56. R3 (persisted state must be consumed) sharpens P3 (canvas reachability).
- **Doc 57 (Capstones)** — Pattern B branching capstones are the T1 / T3 implementation form when the fork is large enough to script both paths as full scenes. Doc 70 §6.1.2 (A) wire-it remediation is the upgrade path from a Phase 2+ seed flag to a Doc 57 Pattern B capstone.

### §8.2 — Phone-system architecture siblings (Doc 70 applies on top of these)

- **Doc 42 (RTS Phone System Reference)** — what RTS's phone actually is: purchase-gated device, modal app launcher (not passage nav), dispatch bus that re-evaluates triggers every render, daily cadence, corruption-axis escalation. Doc 70 doesn't re-document any of this; it specifies click-level rules INSIDE these structures.
- **Doc 43 (Engine Phone As-Built)** — what the engine supports today (`v2.py:1494–2166` runtime block, `template_import.py:1593–1696` schema). Doc 70 §6 remediations use only fields documented here — no new engine work required.
- **Doc 44 (RTS Phone Parity Gap PRD)** — G1–G12 gap spec. Closed by Doc 45. Listed for historical context.
- **Doc 45 (100% RTS Phone Parity PRD — SHIPPED 2026-05-22)** — all 12 gaps closed including real quest primitive (G4), delay queue (G5), social posting (G2), photo actions (G3), gallery (G8), custom apps (G12), fast jobs + bank (G9), in-world purchase (G11), notifications (G1), corruption tiers (G7). Doc 70 T1/T2/T3 implementations route through these engine primitives.
- **Doc 46 (TLS Phone Design — SHIPPED 2026-05-22)** — TLS's specific chat-centric implementation. **Doc 70 §4.3 corrects Doc 46's flag-provenance framing** for the Frank `keep_route_*` flags (Doc 46 framed them as "existing seed flags" but Docs 19/20 had retired them). Doc 70 §6.1.1 prescribes the cleanup.

### §8.3 — Provenance-trace siblings (cited by §4.3)

- **Doc 02 (NPC Stage Chains)** — original design source for `frank_keep_route_*`. Superseded for Frank by Doc 19.
- **Doc 19 (Frank Stage 3+ Design)** — retired `frank_keep_route_*` flags ("No `frank_keep_route_*` flags"). Authoritative on Frank Stage 4 surface.
- **Doc 20 (Frank Slice RTS Doctrine Review)** — flagged the orphaned `frank_keep_route_*` declarations for removal. Cleanup queued but never executed.
- **Doc 58 (Ryan Design Brief)** — explicitly seeds `ryan_keep_route_*` as Phase 2+ branch outcomes. Authoritative on Ryan keep-route intent.
- **Doc 65 (Phase 2+ Strategic Scope)** — Phase 2+ hold decisions. §6.1.2 (A) "wire it now" violates this hold; (C) "formally defer" respects it.

---

## §9 — Appendix: choice-density target ratios

Soft targets, not hard limits. Use as smell-tests during audit, not as enforcement.

- **Forks per canvas: 0–1 typical.** Hub canvases excluded (those use tier-gated rungs per R4, not forks per R5). A canvas with 2+ flagEffects-bearing forks is almost certainly violating R5 — collapse or capstone-promote.
- **Cascade beats per scene: 3–8 typical.** Match RTS scene-cascade scale (`SellingMyStepsister` has 17, but that's the upper end for a fully-scripted Stage-4 explicit beat; ordinary Lane 2 ambients should sit at 3–5).
- **Phone reply forks per slice: ≤ 1 per NPC arc.** Each MUST satisfy T1, T2, or T3. The current TLS slice has 9 phone forks total; only 1 (`anon_dm_seen`) is compliant.
- **RTS reference ratio: 6% fork-to-beat.** TLS should approximate this. A slice with >15% fork-to-beat is over-forking; the player can't tell which forks matter.

---

## §10 — Open questions surfaced (not blocking)

- **Validator extension (potential Doc 71):** A Phase-3 validator that checks every `flagEffects = [{ flag = "X", op = "set" }]` has at least one corresponding `flag_key = "X"` reader somewhere in the template. ERROR severity on zero readers. Would mechanism-prevent the dead-flag-fork pattern at build time. Not authored here; queue as Doc 71 PRD if LO wants the engine enforcement.
- **Trait-band consumer audit:** the 5 trait-only phone forks would become T5-compliant if downstream canvases gated on trait bands (love ≥ 5, trust ≥ 8, etc.) at the post-Stage-2 timing window. A trait-band-consumer audit per NPC could surface exactly which thresholds need authoring. Out of scope for Doc 70.
- **Quest-card consumer wiring:** TLS quest_cards (PRD 48 / Doc 50) are the natural T1-consumer surface for wired phone forks. Authoring the (A) wire-it remediations would touch the quest_cards section of `7_final_game.toml`. Doc 70 doesn't prescribe which cards to add — that's per-fork authoring work.

---

## §11 — TLS slice issues PARKED 2026-05-27

**LO decision 2026-05-27:** stop further TLS slice remediation in this session. The slice is engine-validation infrastructure (Doc 30 §8.2 — "not a player-facing game; dev shortcuts visible"), not a shipping product. Remaining issues catalogued below are NOT being fixed — they are explicitly accepted as known state. Re-evaluate when/if the slice becomes player-facing or when Phase 2+ resumes (Doc 65).

### §11.1 — Doc 70 §6.2 trait-only forks (5 phone fork pairs) — PARKED

Five inline `choices = [...]` blocks set NO flags, only trait deltas. Each violates T1–T5 (the trait deltas land in bands nothing currently gates on). Doc 70 R5 prescribes collapse. NOT collapsed in this session.

| Phone conversation | Trait deltas | Why parked |
|---|---|---|
| `frank_after_office` | +2 love OR +2 corruption | Thread is DORMANT in slice (`frank_office_first_sex_done` never set in scope). No player exposure. |
| `jake_sorry` | +3 trust OR (+2 corr, +1 corr) | Jake arc held at Stage 1 in slice; chat fires post-`jake_peek_draw_revealed`. Deltas don't reach any active gate. |
| `jake_tease` | (+1 arousal, +1 corr) OR +2 trust | Same as above. |
| `ryan_thanks` | +3 trust OR +3 love | Most defensible to keep — +3 trust feeds Stage 0→1 (`trust >= 10`) but chat fires AT Stage 2 (timing-misaligned). |
| `anon_2` | (+3 corruption) OR (+1 calculation) | `calculation` trait declared but unused at slice scale. Phase 2+ scaffolding. |

**State:** flagEffects-free already (only trait deltas), so no dead-flag pollution. The forks are flavor-shaped but mechanically inert at slice scale. Acceptable for engine-validation slice.

**Re-evaluation trigger:** if any of these chats become player-facing (slice promoted past engine-validation status), apply Doc 70 R5 collapse OR author trait-band consumers per §10 audit.

### §11.2 — Pre-existing build warnings — ACCEPTED

The `package_from_toml` build emits warnings unrelated to phone choice cleanup. Catalogued here so future audits don't mis-attribute them to Doc 70's edits.

#### §11.2.1 — Trait-effect extraction warnings (~13 unique canvases, fires 2-3× each)

```
WARNING Error extracting trait effects from canvas 'X': '>' not supported between instances of 'dict' and 'int'
```

Affected canvases (Frank Lane 2 ambients + Lane 3 substitutions + Lane 4 bedroom):
- Kitchen — Frank's hand while you pour / squeezing past Frank / Frank arrives while you're making coffee / Frank passes the door while you're making tea
- Living room — Frank on the couch / Frank joins you on the couch
- Yard — Frank washes off at the spigot / Frank shirtless on the fence / pulled into the toolshed
- Back porch — Frank joins you at the railing
- Bathroom — Frank in the doorway
- Frank's bedroom — sex loop / climax

**Diagnosis:** code-path issue in the trait-effects-extraction validator (template_import.py side). The `'>'` comparison fails when one operand is a dict (likely a full effect object) and the other is an int. Pre-existing across sessions; not introduced by phone choice cleanup. Likely a Doc 69 validator extension blind-spot — could be picked up under Doc 71 if/when authored. **Does not affect generated HTML output** (build completes, package emits).

#### §11.2.2 — Missing location images (~18 locations)

```
WARNING Location image not found: locations/X.jpg for Y
```

All 18 location images missing. Per Doc 46 §11 and Doc 30 §8.2 — TLS slice ships without location art intentionally (engine-validation surface, not player-facing). No remediation needed unless slice is promoted.

#### §11.2.3 — Repeatable canvas overlap (1 structural)

```
WARNING Repeatable canvases 'scene_franks_bedroom_evening' and 'scene_franks_bedroom_setter' both trigger
for NPC 'npc_frank' at location 'loc_franks_bedroom' with overlapping schedules.
```

Pre-existing structural warning. `scene_franks_bedroom_evening` is the T3 anchor capstone (Doc 19 §5); `scene_franks_bedroom_setter` is the dev/setter mode entry. Both are intentional — setter mode is gated by a dev shortcut, runtime resolution picks one. Engine warns because the static-graph analyzer can't see the dev-flag gating. Cosmetic; accepted.

### §11.3 — General slice state acknowledgement

The TLS test slice (`games/the_long_summer_test/`) has known imperfections beyond the items above (dev-only Stage 2+ Ryan/Jake/Frank advancement, deferred Diana confrontation branches per Doc 60, Cookie/Marge sketched but Phase-3-deferred per Doc 61, missing art assets). These are documented across Docs 30, 46, 60, 61, 65 and are NOT defects relative to slice scope.

**Doc 70 explicitly stops auditing the slice past the Cᴿ cleanup (§6.1.1) + Cˢ defer (§6.1.2 / §6.1.3) executed 2026-05-27.** Future Doc 70-driven slice work resumes only on explicit LO direction or when Phase 2+ unblocks.
