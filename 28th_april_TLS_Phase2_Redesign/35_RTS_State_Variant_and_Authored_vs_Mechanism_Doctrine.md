# 35 — RTS State-Variant Routing & Authored-vs-Mechanism Doctrine

> **Status:** Doctrine record from a live analysis session. No code changed — read-only investigation + synthesis.
> **Session:** 2026-05-18, 18:21 IST (Monday). Single conversation, started from "explain Frank content in simple words" and walked down to a source-grounded pregnancy-flag trace.
> **Purpose:** Capture two confirmed structural lessons + four additions about how RTS treats NPC progression and story, and pin the TLS Frank ↔ RTS divergence so future NPC work (Ryan/Jake/Diana) inherits the corrected mental model — not the loose one.
> **Method:** Re-read docs 21 + 22 (source-extracted RTS mechanism audits). Then a direct trace of the pregnancy flag through the RTS capture artifact (`game_explorations/rts-arc-trace/`): `passage_catalog.json` (361 passages, source_raw), `variable_index.json` (131 indexed vars + complex setters). Per methodology rule §N: structure is extraction-answerable; the one JS-resolved gap is flagged honestly, not guessed.

---

## §1 How the session got here (question chain)

The conversation walked a deliberate ladder, each answer narrowing the next question:

1. Explain Frank's 3 lanes + progression in plain words.
2. Is that how RTS progresses NPCs? → forced the honest divergence answer.
3. What are Frank's "3 named milestones"? → `frank_caught` / `frank_bedroom_first_done` / `frank_cracked`.
4. What are RTS Brother's three milestones? → **trick answer: Brother has none** (stat gradient, not a milestone spine).
5. That's all mechanics — what about *story*? → authored-vs-systemic distinction surfaced.
6. But RTS has story after pregnancy, right? → user's instinct was correct; my first "RTS barely has story" was too flat and got corrected.
7. Trace the pregnancy flag. → the source-grounded evidence in §4.
8. Here are the lessons — am I right? → this doc.

The ladder matters: the doctrine below is only trustworthy because each rung was checked against source before the next was claimed.

---

## §2 The two confirmed takeaways (tightened)

The user proposed two. Both hold. Each needed one sharpening so it generalizes instead of overclaiming.

### 2.1 Persistent global states variant-route content across NPCs

**Loose version (the user's):** "all major NPC canvases change based on states like pregnancy."

**Precise version (what source actually shows):** RTS does **not** mutate a scene in place for a state. It keeps the base scene and routes to a **separate variant passage** when a state predicate passes:

- `BrotherBedroomSex1` → `BrotherBedroomPregnantSex1`
- `DadShowerSex` → `DadShowerSexPregnant`, `DadWashDishesSex` → `DadWashDishesSexPregnant`
- `MarcusBedroomSex` → `MarcusBedroomSexPregnant`
- plus stage-keyed event routing: `BathroomMorningSickness` (early), `BathroomBellyAwareness` (showing), `BathroomLactation`

The state does not rewrite the canvas; the state **selects which canvas**. The portable primitive is *persistent-state-keyed variant routing*, not in-place mutation.

**Scope honesty:** confirmed for Brother / Dad / Marcus (Edward thinner) — ~30% of the RTS catalog sampled across docs 21+22. Not "all NPCs."

**The bigger lesson under it:** pregnancy is not special — it is the loudest case of a general rule. Boyfriend status (`MakeBoyfriend`), corruption *level*, arousal, and `pregnancy.discovered` are all persistent states content branches against the same way. RTS runs on a small set of persistent states; content is variant-routed against them.

### 2.2 Authored vs mechanism — the dividing line

**The user's instinct:** RTS uses authored content for one kind of story and full mechanism for another.

**The boundary, stated exactly (from the trace):**

| Layer | What RTS uses | Examples from source |
|---|---|---|
| **Mechanism (systemic / emergent)** | Anything that *repeats* | Corruption-meter → scene-unlock loop; daily texture; the pregnancy *system* (stages, symptoms, `pillDays` contraception, JS conception roll) |
| **Authored (scripted / placed)** | The *points of no return* and *real-choice forks* | `PregnancyTest` discovery scene; prenatal / Doctor questline; Pattern F branches (`SellingMyStepsister`, `MarcusParkDate` Accept/Decline) |

**One-line rule:** *RTS mechanizes what repeats; it authors the irreversible turning points and the forks.* This is directly applicable to any new TLS content — ask "does this repeat?" → mechanism; "is this a point of no return or a real choice?" → author it.

---

## §3 Four additions the trace surfaced (all source-grounded)

1. **Fact/awareness is a deliberate two-flag primitive.** RTS splits `$player.pregnancy.isPregnant` (it is true) from `$player.pregnancy.discovered` (Maya *knows*). The gap between them *generates* the suspicion beat — `SleepWidget` narrates nausea + "maybe buy a test" only while `isPregnant() && !discovered && hasPregnancySymptoms()`. **TLS Frank has no equivalent "she suspects but doesn't know yet" layer.** A state and the character's knowledge of it can be two flags; the space between them is free drama.

2. **Authored ≠ long.** The authored hinge — `PregnancyTest` — is a handful of lines (`<<if isPregnant>><<set discovered = true>>` + stage-keyed text). The *system* around it is large. "RTS authors the turning points" does not mean "RTS writes volume there." It spends one short scripted scene at the hinge and lets mechanism carry the rest. Corrects the assumption that authored content = prose density.

3. **One state, multiple on-ramps.** Pregnancy is reachable two ways: natural conception (JS, post-sex, resolved at sleep) **and** a corruption-gated clinic route (`SexualInsemination` / `ArtificialInsemination` / `ClandestineClinic`, gated `getCorruptionLevel() >= 3`). The same milestone has more than one fictional door. TLS Frank's milestones are single-route (one catch, one first night). A milestone can have several narrative paths in.

4. **Heavy content can be an opt-in track.** `$player.pregnancy.enabled` is set in exactly one place — `Menu`, ungated. The entire arc sits behind a player toggle. Divisive or heavy systems need not be forced into every playthrough; they can be a switchable lane.

---

## §4 The pregnancy-flag trace (evidence)

Concrete, so this doc stands on its own without re-running the trace.

**Fields (from `variable_index.json`):**

| Field | Set where | Gate on the setter |
|---|---|---|
| `pregnancy.enabled` | `Menu` only | none (player toggle) |
| `pregnancy.isPregnant` | **JavaScript** (StoryJS, not a twee passage) — index marked it complex/skipped | natural: `enabled` + creampie state + chance at sleep; alt: clinic route |
| `pregnancy.discovered` | `PregnancyTest`; `HospitalPregnancyTest` | `isPregnant` (+ `money >= 30` for hospital) |
| `pregnancy.pillDays` | `Bathroom`, `ApartmentBathroom` (`+= 3`) | `contraceptivePill > 0` && `!isPregnant` |
| insemination state | `SexualInsemination` (complex setter) | `getCorruptionLevel() >= 3` |

**What `isPregnant()` gates (reads, from `passage_catalog.json` source_raw):**

- `SleepWidget` — stage-keyed wake text; the symptom→suspicion nudge
- `Bathroom` / `ApartmentBathroom` — morning sickness / belly-awareness / lactation events, gated by `getPregnancyStage()` (`early` / `showing` / further)
- `ClassroomEvent` — `hasVisibleBelly()` swaps content
- `BrotherBedroom` and the `*Pregnant` scene variants across Brother/Dad/Marcus
- Walkthrough objectives (quest strings in the index): *"Get pregnant and go to the hospital for prenatal care and have 3 relation points with the Doctor"*; *"…have sex with him while being pregnant"*

**Honest gap:** the exact natural-conception trigger is in StoryJavaScript, not in any passage's `source_raw`, so the dice/chance was **not** observed. Birth / post-baby content was **not** traced (stages seen: `early`, `showing`, "quite far along"; no birth scene confirmed either way).

---

## §5 TLS Frank ↔ RTS — the divergence, pinned

So future NPC work doesn't re-derive this from scratch:

| Axis | RTS (Brother, family-proximity) | TLS Frank |
|---|---|---|
| Progression spine | Continuous corruption *level* + per-NPC stage helper (`StageTwoCorruption`) + ~16 per-scene completion flags | **3 named milestone flags**: `frank_caught` → `frank_bedroom_first_done` → `frank_cracked` |
| Content topology | ~16 *distinct* per-location cascades, never collapsed | One shared `loop_franks_bedroom_sex`, 5 hub entry points (deliberate slice consolidation) |
| Lane weighting | Lane-2-heavy (random encounters carry the bulk; Pattern D dominant) | Lane-1-deliberate (5 location hubs are the content surface) |
| Story delivery | Systemic — states + one scripted hinge (pregnancy test) | Authored — 3 scripted hinge scenes placed for dramatic shape |
| Cascade shape | Pattern D for family arcs (correct match) | Pattern D `[group]+[cascade]` — faithful |
| Hub buttons | Render by presence+time; stat gate in click-handler; notify-on-fail | `show_when_locked` + notify-on-click — faithful to the *corrected* RTS model |

**Verdict:** the vocabulary (3 lanes, greyed-ladder-with-notify, Pattern D for family) is genuine RTS, correctly ported. The *spine* (3 milestones vs stat gradient) and *topology* (one loop vs per-location distinct scenes) are intentional TLS slice simplifications — cleaner to author, less granular than RTS's drip. Not a bug; a known, deliberate trade.

---

## §6 Confidence ladder

✅ **HIGH (source-verified this session):**
- Pregnancy variant-routing across Brother/Dad/Marcus
- `discovered` / `pillDays` / `enabled` setters + gates (variable index)
- `isPregnant()` read sites (passage source_raw)
- The authored-vs-mechanism boundary as stated in §2.2

🟡 **MED (inferred, consistent with source but not directly observed):**
- Natural conception = creampie state + chance at sleep (shape inferred from `SleepWidget` + `pillDays` logic; exact JS unseen)
- "Most NPCs" variant coverage — confirmed for a 30% sample, not the full catalog

❌ **NOT established:**
- Exact conception dice/chance (StoryJS, not in artifact)
- Birth / post-baby / child content existence
- Whether unaudited NPCs (Sam, Emma, Jamal, Veronica, Priest, etc.) follow the same variant-routing

---

## §7 Portable recommendations for TLS

Not committed work — candidates for when NPC depth is prioritized:

1. **Adopt the fact/awareness split** for at least one Frank or Diana beat (a state + a separate "Maya knows" flag) — it manufactures a suspicion arc cheaply, which the slice currently lacks.
2. **Treat authored beats as short hinges, not prose dumps** — keep the RTS-flat scene-body doctrine; the milestone's job is placement, not length.
3. **Consider a second on-ramp** to one Frank milestone (e.g., the catch reachable via a second situation) to reduce the single-route brittleness.
4. **Stop calling RTS purely systemic** — the corrected model is "systemic loop + authored points-of-no-return + a few real forks." Carry that phrasing into Ryan/Jake/Diana design so they get authored hinges, not just escalation ladders.

---

## §8 Source artifacts

- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — 16 Brother passages, patterns A–F
- `28th_april_TLS_Phase2_Redesign/22_RTS_Cross_NPC_Mechanism_Comparison.md` — Dad/Marcus/Edward, ~40 surfaces, §11 live verification
- `game_explorations/rts-arc-trace/passage_catalog.json` — 361 passages, source_raw (captured 2026-04-29)
- `game_explorations/rts-arc-trace/variable_index.json` — 131 indexed vars + 5 complex setters
- This session's trace commands reproducible against the two artifacts above

---

End of doctrine record.
