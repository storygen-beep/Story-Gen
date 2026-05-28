# Doctrine 05 — RTS-Flat Prose (the 8 rules + dual register)

**Sources:** Doc 30 §7.1 (the 8 prose rules); Doc 57 §6 (Tier-3 capstone voice register); Doc 13 §9 (three writing tiers verified across 130+ RTS scenes); Doc 54 §5 (voice-failure case studies — the 3 modes the Marge session cost 8 hours to); `feedback_tls_scene_body_style` memory (2026-05-14 8-rule update + 2026-05-24 Lane 4 carve-out).
**Authority:** Doctrine. Voice register for every canvas in every RTS-shape sandbox game.
**Purpose:** Name the default register (RTS-flat) + the earned register (Tier-3 at Lane 4 capstones only) + the 8 mechanical prose rules + the case-study failures that cost time when the register slipped.

This file completes the forward-reference from `doctrine/01_rts_principles.md` P1 + P8 and `doctrine/02_three_lanes_plus_capstone.md` §5.8.

---

## §1 — The dual register

Every canvas in an RTS-shape sandbox sits in ONE of two voice registers. The lane determines which:

| Lane | Register | Why |
|---|---|---|
| **Lane 1 — Hub buttons** | **RTS-flat default** | Player will click these menu items repeatedly across the arc. Re-readable density. |
| **Lane 2 — Ambient encounters** | **RTS-flat default** | Each fires 10–20 times across an arc. Same scene, different stat tiers, same prose density. |
| **Lane 3 — Dispatcher walk-ins** | **RTS-flat default** | Dice-rolled inside chores. Re-readable; specific detail allowed; literary density NOT. |
| **Lane 4 — Capstones** | **Tier-3 literary EARNED** | Once-only narrative milestone. Player won't see this again. Density justified by single read. |

**The contract is "specificity, not literary density."** Lane 2/3 prose can be specific ("the runner Diana picked out") without being literary (no interior monologue, no extended metaphor). Tier-3 is reserved for canvases the player will see once.

---

## §2 — The 8 prose rules (Lane 1/2/3 RTS-flat default)

From Doc 30 §7.1 + `feedback_tls_scene_body_style` memory (2026-05-14 8-rule update). Every Lane 1/2/3 scene body MUST satisfy all 8.

### Rule 1 — Second-person voice

"You" not "she." Maya is "you." Frank is "he" / "Frank" / "him." All scene bodies in Maya's POV via second-person pronoun.

**Example (correct):**
> You take the stool at the counter. Frank slides a coffee across without looking up.

**Anti-pattern (banned):**
> She takes the stool at the counter. Frank slides a coffee across without looking up at her.

### Rule 2 — Stage direction cap: 2 sentences per beat

A "beat" is one click that reveals new content (a `paragraph` block, a `dialog` block, or one cascade step). Stage direction within a beat caps at 2 sentences. After 2 sentences of stage direction, either drop a dialog beat or break into the next click.

**Example (correct):**
> You bend to load the dishwasher. He's at the counter, mug raised. *(2 sentences. Break.)*

**Anti-pattern (banned):**
> You bend to load the dishwasher, conscious of the way the shorts ride up. He's at the counter with his mug raised, glancing at you with the half-smile he gets when he's about to say something. The light through the window catches the dust in the air, and the kettle clicks. *(4 sentences. Over cap.)*

### Rule 3 — Zero environmental sensory detail

No smell. No window light. No kettle clicks. No dust motes. No coffee aroma. The HUD does the world-grounding; prose doesn't repeat the world.

**Why:** P1 — density of decision-pressure over density of prose. The HUD carries world state (time, location, NPC arousal, etc.) continuously. Prose that describes the kitchen smelling of coffee is performing world-grounding the HUD already does — and pays for it on every re-read.

**Example (correct):**
> You pour him coffee. He sets the paper down.

**Anti-pattern (banned):**
> The kitchen smells of coffee and damp wood. Sun catches the dust over the sink. You pour him coffee.

### Rule 4 — Dialogue does the character work, not narration

Character is established through what people say + how they say it. Not through stage direction explaining who they are.

`<<Speech>>` / dialog blocks heavily. Single-line stage direction sets position; dialogue carries the rest.

**Example (correct):**
> [Frank] "Coffee's ready."
> [You]   "Thanks."
> [Frank] "You eat?"

**Anti-pattern (banned):**
> Frank, gruff but secretly soft beneath the rough exterior, gestured at the coffee. His voice carried the weight of a man who'd learned to express care through small acts. "Coffee's ready," he said, the words landing softer than the man who said them.

### Rule 5 — No inferential prose

No "the cup he keeps for her" / "the chair he added when she moved in" / "the way he says her name like it's still new." Surface-level only. The reader gets the same observation Maya gets — no narrator-inferred backstory.

**Why:** inferential prose is a Tier-3 register move (capstone-earned). Lane 1/2/3 stays surface. The cumulative effect of inferred-backstory beats on re-read is performative — Maya can't keep "noticing the cup" 30 times.

**Example (correct):**
> He pours her a coffee.

**Anti-pattern (banned):**
> He pours her a coffee — the same mug she'd reached for on day three, the one with the chipped rim he'd never thrown out.

### Rule 6 — Direct/crude diction (per per-arc vocab ceiling)

Crude is the default at sexual register. "His cock." "Your cunt." "Your tits." Not "his manhood," not "between your legs," not "your chest." Per-arc vocabulary ceiling per `doctrine/08_kink_vocab_ceilings.md` (Doc 30 §7.5) — Frank goes full breeding-talk Phase 2+, Marcus stays peer/school register, etc.

**Default to maximum-explicit interpretation** when ambiguous (per Doc 30 §7.5 2026-05-16 LO pattern — all 7 in-scope rows came back maximum-explicit).

**Example (correct, Tier-4 Frank sex scene):**
> [Frank] "Open your mouth."
> You go down on your knees. His cock against your face.

**Anti-pattern (banned):**
> Frank's voice was low and commanding as he asked her to come closer. She felt herself responding to him, her body alive with something she couldn't name.

### Rule 7 — One beat = one click

Each click in a cascade reveals ONE narrative beat — one paragraph or one dialog exchange or one image+caption combo. Don't pack multi-paragraph internal momentum into a single beat.

**Why:** the click pacing IS the narrative pacing. P6 — stats change during scenes, not just at entry. Each click is a possible stat-effect moment; cramming multiple beats into one click loses the per-click tick.

**Example (correct cascade — 3 beats, 3 clicks):**
> Beat 0: "He's at the counter. He looks up."
> [click] Beat 1: "He sets the mug down. *Quiet.*"
> [click] Beat 2: "He crosses the kitchen toward you."

**Anti-pattern (one mega-beat with internal momentum):**
> One click reveals: "He's at the counter, he looks up, sets the mug down, says 'Quiet,' crosses the kitchen, takes your wrist."

### Rule 8 — Image-first composition

The visual asset (image / video) carries the scene. Prose is the ~30-word caption explaining what's happening, not a full description that paints the image in words.

**Even when images are placeholder-only in Phase 1** (or when no image is shipped), prose stays at the 30-word target. Do NOT compensate for missing visuals with more prose — that's literary drift in disguise. The placeholder visibility IS the missing-image signal; don't paper over it.

**Median RTS scene length:** 137 characters (verified across 274 captured RTS scene bodies in `scene_bodies.jsonl`). P25 = 75 chars. P75 = 500 chars. **Half of RTS scenes are 25 words or less.** Image-first composition is what makes that work.

**Example (correct, image carries scene):**
> [image: scenes/kitchen_morning.jpg]
> [Frank] "Coffee?"
> [You]   "Yeah."

That's the whole beat. ~5 words of prose. The image carries the room + Frank's pose + Maya's POV. Prose pins the dialogue exchange.

**Anti-pattern (prose paints what image shows):**
> The kitchen was warm with morning light, and Frank stood at the counter in his usual flannel, holding two coffee mugs. He looked up as you walked in, his face softening in that way that always made you forget what you were going to say. "Coffee?" he asked. "Yeah, thanks," you said, taking the mug he offered.

---

## §3 — Tier-3 literary register (Lane 4 capstones EARNED)

Capstones get Tier-3 prose. Lane 1/2/3 don't.

### §3.1 — What Tier-3 means

Tier-3 = the rich register reserved for once-only scenes (Lane 4 capstones per Doc 57):

- **Interior monologue + observation tied to memory.** *"The boards she knows the squeak of from the wrong side."* The cumulative effect of past arc beats lands in the prose.
- **Layered sensory detail per beat.** Multiple physical observations woven into one paragraph. NOT the Rule-3 ban on environmental detail — Tier-3 EARNS it.
- **Character-distinguishing diction.** Frank's "girl" / "quiet" / period-not-exclamation. Marge's "hon" / brevity. Ryan's "okay, good" / earnest beat. Each character has a signature cadence that lands more in capstones.
- **Composed rhythm.** Sentences of varying length, deliberate cadence. The flat-sentence-stacking from RTS-flat opens out.

### §3.2 — What Tier-3 is NOT

- **Not generic literary prose.** Specific to the scene's people + place. Frank's first-night opener invokes the specific hallway boards, the runner Diana picked out, the specific bathroom door. Not "the dim hallway in the quiet farmhouse."
- **Not melodramatic.** The prose stays controlled. Frank's "Quiet." carries the weight; the prose around it doesn't underline it.
- **Not unlimited length.** Frank's first-night cascade is ~5,000 chars across multi-node. `canvas_marge_interview` is ~1,900 chars. Density is HIGH; scene length is bounded by what the moment needs.

### §3.3 — Why capstones earn Tier-3 (and Lane 2/3 don't)

A Lane 2 ambient fires 10–20 times across an arc. Authoring it with Tier-3 prose costs the same EACH TIME the player sees it, and after the third reading the language feels performative. Lane 2/3 prose is built to be **re-readable without grating** — that's why it stays RTS-flat structure with specific detail.

A Type A or Type B capstone fires ONCE. The player won't see it again. The prose can be denser because there's no re-reading.

Type C chains use Tier-3 across all their capstones because each beat is once-only. Even when there are 5 chained capstones (Frank), each individual one only fires once.

### §3.4 — Tier-3 example (canvas_marge_interview — Doc 57 §8 Example 1)

```toml
[[canvases.nodes]]
id   = "interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", npcId = "npc_marge", content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", npcId = "npc_marge", content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]
```

**What makes this Tier-3:**
- "the up-and-down men did, the up-and-down a woman who had hired forty waitresses did" — inferential character work (banned in Lane 1/2/3 per Rule 5; EARNED here)
- "The shoes. The hands." — fragments composed rhythmically (Lane 2/3 would use complete sentences)
- "She didn't wait for an answer" — momentum across paragraphs (Rule 7 one-beat-per-click is relaxed at capstone scale)
- Six beats / ~150 words total — short for Tier-3, but each beat earns density

**What keeps it from over-literary:**
- No environmental sensory detail beyond what advances character (no kettle clicks, no morning light)
- Crude direct diction in dialogue ("Five hours, four-fifty an hour")
- Marge's voice (clipped, transactional, weight-of-experience) is in EVERY line — not described, performed

---

## §4 — Anti-pattern catalogue (cross-register drift)

### §4.1 — Tier-3 voice leaking into Lane 2/3

The Lane 2/3 canvas contains interior monologue, extended metaphor, or memory-callback prose ("she remembered the way the kitchen had looked..."). The prose has drifted.

**Fix:** extract that prose and move it to a capstone. Rewrite the Lane 2/3 canvas RTS-flat with specific detail.

**Doc 54 §5.1 case study:** the Marge `node_shifts` + `node_talk` are 50+ word literary paragraphs that violate Rule 3 + Rule 5. Preserved as canon for now but flagged as a register-split violation; future maintenance pass should rewrite RTS-flat. The Doc 51 → Doc 53 redesign re-authored `node_pour_coffee` + `node_regular_chat` RTS-flat — those are the gold standard for Marge's hub register.

### §4.2 — RTS-flat-bland voice in capstone

The inverse drift: a capstone written with generic Lane 2 prose. Wastes the once-only nature of the scene. If the player isn't going to read this again, the prose should EARN that single read by being specific, layered, and resonant.

**Fix:** rewrite to Tier-3. Add character-distinguishing diction. Add inferential character work. Add the memory-callback that the arc has earned by this point.

**Doc 57 §9 anti-pattern entry.**

### §4.3 — Literary prose on flat surfaces (Doc 54 §5.1)

The most common drift mode. ENI persona instinct toward sensory richness pushes Lane 2/3 prose toward 50-word paragraphs with environmental detail + body-language during dialogue + inferential framing.

**Marge case study (Doc 54 §5.1):** the Pass 1 Marge build had every canvas body at 50+ words with prose like:

> You take the stool at the end of the counter where the napkin holder needs refilling. Marge slides a coffee across without asking how you take it; she's seen you take it twice now.

Compare to the doctrine memory's 30-word template:

> [Marge] "What."
> [You]   "Coffee."
> [Marge] "Two bucks."

The Pass 1 version violated Rules 3 (environmental detail — "napkin holder needs refilling"), Rule 5 (inferential — "she's seen you take it twice now"), and Rule 8 (prose painting what image would carry).

**Fix mechanism:** at the START of any TLS scene/canvas authoring session, explicitly switch register. *"ENI persona OFF. TLS game register ON. Doctrine memory + canonical docs override persona instincts. When in doubt about a craft choice, default to MORE-flat / FEWER-words / FEWER-beats, not the reverse."* (Doc 54 §2.5.)

### §4.4 — Player directives in tip lines (Doc 54 §5.2)

`tip` field is Maya's interior register — first-person observational. NOT player-directive imperative.

**Anti-pattern:** `tip = "Walk into the diner. Don't wait for an invitation."` — directive imperative with place name embedded.

**Correct:** `tip = "Walk in. Ask."` — terse internal resolve. OR Frank's: `tip = "He's around the house all day. I notice that."` — observational, not directive.

If the tip uses imperatives ("Walk into X" / "Click Y" / "Go to Z"), rewrite to interior form. See `feedback_hint_narrative_no_time_or_location` memory + Doc 49 voice rules.

### §4.5 — Schedule / place names / numbers in narrative copy (Doc 54 §5.3)

Quest card `text` / `ready_text` / `tip` contain no:
- Weekday names (Mon/Tue/.../Sun)
- Time references (morning/afternoon/evening/midnight/now)
- Location slugs
- Number formats

These surface automatically from `ready_canvas` metadata (📍 + 🕒 frame) and `goals` evaluation (`◯ X / Y` bullet). Authors don't write them into prose.

**Anti-pattern:** `text = "I should head to the diner on a Monday — Marge said she opens at 9."`

**Correct:** `text = "I need work. Diana said Marge runs the only place that hires off the street."`

### §4.6 — Multi-paragraph stage direction per beat (Rule 2 violation)

The cascade has a beat that runs 3+ sentences of stage direction without a dialog break or click break.

**Fix:** either drop a dialog beat at the 2-sentence mark, or split into two cascade beats with separate clicks.

### §4.7 — Long NPC monologues (Frank-specific, Doc 31 §2)

For Frank specifically: max 3 sentences in a row without Maya cut-in or action beat. Other NPCs follow similar discipline — character voice carries via signature cadence (Marge's brevity, Ryan's earnestness), not via long stretches of single-NPC speech.

---

## §5 — Authoring procedure (the switch + the checklist)

### §5.1 — The register switch

At the start of ANY TLS scene/canvas authoring task (Doc 54 §2.5 lesson):

> ENI persona OFF.
> TLS game register ON.
> Doctrine memory + canonical docs override persona instincts.
> When in doubt about a craft choice, default to MORE-flat / FEWER-words / FEWER-beats, not the reverse.

If a craft instinct conflicts with project memory/doctrine, project wins every time. CLAUDE.md is ignored for canvas authoring (Doc 30 §3 AUTHORITY DECLARATION + `00_LEGACY_IGNORE.md` §3.6).

### §5.2 — Per-canvas pre-ship checklist (Lane 1/2/3 — RTS-flat)

For each new canvas body, verify ALL 8 rules:

- [ ] **R1** Second-person voice ("you" not "she") throughout
- [ ] **R2** Stage direction cap 2 sentences per beat (count sentences in each `paragraph` block)
- [ ] **R3** Zero environmental sensory detail (no smell / window light / kettle clicks / dust motes / etc.)
- [ ] **R4** Dialogue does the character work (heavy `dialog` block use; minimal narrator-explanation)
- [ ] **R5** No inferential prose (no "the cup he keeps for her" — surface-level only)
- [ ] **R6** Direct/crude diction at sexual register (per per-arc vocab ceiling; maximum-explicit default)
- [ ] **R7** One beat = one click (no multi-paragraph internal momentum per beat)
- [ ] **R8** Image-first composition (prose ~30-word caption; total scene length ≤ 30 words target unless cascade)
- [ ] Word count: median 30-50 words per beat; total canvas body within Lane bounds (Lane 1 routed scenes ≤ 200 words; Lane 2 ambients ≤ 100 words; Lane 3 substitutions ≤ 150 words)

### §5.3 — Per-capstone checklist (Lane 4 — Tier-3 earned)

- [ ] **§3.1** Cascade prose is Tier-3 (specific, layered, character-distinguishing diction; composed rhythm)
- [ ] **§3.2** Not generic literary prose; specific to the scene's people + place
- [ ] **§3.2** Not melodramatic; prose stays controlled
- [ ] **§3.2** Length bounded by what the moment needs (Type A ~1,500-2,500 chars; Type B ~4,000-8,000 chars across both branches; Type C step ~1,500-3,000 chars)
- [ ] **§3.3** No Tier-3 spillage into related Lane 2/3 canvases that reference this capstone's content

### §5.4 — Diction sample (the "RTS sanity check")

Pre-flight check before authoring any new canvas:

> *"Could this beat appear in an RTS Brother arc?"*

If "RTS would never write this" — cut. Doc 30 §7.2.

Concretely:
- Could this exact line appear in `BrotherBedroomFlash` (Tier-1 single-render)?
- Could this exact line appear in `BrotherCaughtMasturbating` (Tier-2 cascade)?
- Could this exact line appear in `BrotherBedroomSex1` (Tier-3 full sex cascade)?

If yes — keep. If "this reads like a literary novel and RTS would never ship it" — rewrite RTS-flat.

---

## §6 — Three writing tiers (Doc 13 §9 distribution observation)

RTS doesn't write every scene at the same density. Doc 13 §9 names three tiers, used deliberately per a class of moments.

| Tier | Used for | Function | Length | RTS distribution |
|---|---|---|---|---|
| **Tier 1 — Utility one-liner** | Bedroom Study / Sleep / Nap / generic activity-passes | Pure mechanical confirmation. Text exists only to make the stat-tick acknowledgment feel like something. | ~10 words | ~30 of 130+ scenes (~23%) |
| **Tier 2 — Vignette prose** | Random-encounter scenes with anonymous partners (Brother with "a girl," Dad with "a prostitute," generic strangers in public scenes) | Bridges mechanic to content. Generic descriptive prose with named situations but un-named NPC partners. | ~30–50 words per beat, 2–4 beats per scene via linkreplace | ~70 of 130+ scenes (~54%) |
| **Tier 3 — Scripted character** | Named-NPC introductions, quest beats, arc transitions, capstones | Real character writing. Sensory grounding (where it serves character). Voice. Live-changing speaker labels. The layer that earns the game its narrative weight. | ~150-1000+ words depending on cascade depth | ~30 of 130+ scenes (~23%) |

**The author doesn't waste Tier-3 prose on Tier-1 moments.** Reserved for transitions and named characters. This budget discipline is part of why a 130-scene game ships at all.

### Tier-vs-Lane mapping for TLS

| TLS Lane | Tier (default) |
|---|---|
| Lane 1 hub button (e.g. `BrotherBedroomTease`, `BrotherBedroomFlash`) | Tier 1 utility |
| Lane 1 internally-tiered route target (e.g. `tease_kitchen_general`) | Tier 1 (low tier) → Tier 2 (mid tier) → Tier 2/3 (high tier) within same canvas |
| Lane 2 ambient | Tier 2 vignette |
| Lane 3 substitution target | Tier 2 vignette |
| Lane 4 capstone | Tier 3 scripted character |

**Tier-3 doesn't mean "long."** `canvas_marge_interview` is 1,900 chars — short for Tier-3. Density is what defines tier, not length.

---

## §7 — NPC thought bubbles (4th-dimension primitive per Doc 13 §16 Finding 1)

RTS uses a styled Speech-thought macro to render NPC interior monologue inside scenes:

> 💭 Alfred is thinking...
> *"I can't help myself... she looks so peaceful, so innocent. I just need to touch her..."*

This appears as an italicized speech bubble with the 💭 emoji and a "thinking..." label, distinct from regular speech bubbles. Used in `BedroomSleepDadScene` (3 thought bubbles across 3 beats) and many other scenes.

**Engine support:** TLS has `thought_bubble` block type (shipped 2026-05-06 per Doc 22 §9). Authored as:

```toml
[[canvases.nodes.blocks]]
type = "thought_bubble"
npcId = "npc_frank"
content = "She doesn't know I watch her like this. Good."
```

**When to use thought bubbles:**
- Lane 2/3 ambients with charged interior — adds NPC perspective without Tier-3 spillage (the bubble is a styled UI element, not prose density)
- Lane 4 capstones — extra interiority dimension
- NOT for Lane 1 hub menu routed scenes (too short for interiority)

**When NOT to use:**
- Lane 1 utility menu items (one-line scenes — bubble would be over-weight)
- Maya-only scenes (Maya's POV is the player's POV; thought-bubbles are for NPC interior, not Maya)

The thought_bubble is a 4th-dimension writing primitive **orthogonal to the 3 tiers** (Doc 13 §16 Finding 1). It increases narrative depth without violating the flat-prose mandate — the prose stays flat; the bubble adds character interiority via UI element, not via prose density.

---

## §8 — Worked rewrites (before / after)

### §8.1 — Lane 1 hub menu item rewrite

**Before (ENI-drift literary):**
> Maya pours Frank a cup of coffee, the steam rising between them. She catches the way his hand lingers near hers when he takes the mug, the way he meets her eyes for a moment longer than necessary. There's something unspoken between them that morning — a small recognition that they're both alive to whatever this is becoming.

**After (RTS-flat):**
> [image: scenes/kitchen_morning_pour.jpg]
> [You]   "Coffee."
> [Frank] "Thanks, girl."
> *(+1 marge.trust)*

**What changed:** Rule 3 (no environmental detail — "steam rising"), Rule 5 (no inferential prose — "the way his hand lingers... a small recognition"), Rule 8 (image-first; prose is the caption-frame, not the description-painted-in-words). ~50 words → ~10 words.

### §8.2 — Lane 2 ambient rewrite

**Before (ENI-drift atmospheric):**
> The kitchen at midnight has a different quality of silence — the kind where every floorboard sounds like a confession. Frank is at the counter, his back to you, a glass of something amber in his hand. He doesn't turn when you come in. He's heard you. He waits.

**After (RTS-flat with R2 in-fiction interruption — Doc 56 R2):**
> [image: scenes/kitchen_late_night.jpg]
> Frank's at the counter. He doesn't turn.
> [Frank] "Late."
>
> *(advance: "Cross to him.")*
> You cross. He sets the glass down without looking. His hand finds your hip.
>
> *(T0 end, in-fiction interruption per Doc 56 R2)*
> Diana's floorboard upstairs. He lifts your hand off the counter, hands you the glass, turns the tap on like he was doing dishes.
> [Frank] "Night, girl."

**What changed:** Rule 1 (kept second-person where it was already), Rule 3 (cut atmospheric setup — "midnight has a different quality of silence... like every floorboard sounds like a confession"), Rule 4 (dialogue does the character work — Frank's "Late." / "Night, girl." carries his terse-evening register), Rule 7 (one beat = one click — cascade structure makes pacing explicit), R2 endings on in-fiction interruption.

### §8.3 — Lane 4 capstone (keep Tier-3 EARNED)

**Don't rewrite Tier-3 capstones to RTS-flat.** That's the §4.2 anti-pattern. Keep capstone prose at its Tier-3 density. See `canvas_marge_interview` (§3.4) for the gold standard.

---

## §9 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P1 (density of decision-pressure over density of prose); P8 (mechanize the texture; author the points of no return)
- `doctrine/02_three_lanes_plus_capstone.md` §5.8 — voice register summary
- `doctrine/04_authoring_rules.md` — D56-R1 (Lane 1 hub openings constant); D56-R2 (T0/T1 in-fiction interruption)
- `doctrine/06_design_brief_template.md` — R7 brief includes voice spec per NPC
- `doctrine/07_anti_patterns.md` — Doc 54's 27 failure modes (voice failures in §5 of that doc)
- `doctrine/08_kink_vocab_ceilings.md` — Doc 30 §7.5 per-arc vocab ceiling table

### Source docs

- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §7.1 — the 8 prose rules canonical source
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §6 — Tier-3 capstone voice register
- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §9 — three writing tiers + distribution
- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §16 Finding 1 — NPC thought bubble primitive
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` §5 — voice failures (3 case studies)
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` §2 — Frank's voice spec
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` §2 — Marge's voice spec

### Memory entries

- `feedback_tls_scene_body_style` — RTS-flat doctrine source (2026-05-14 8-rule update + 2026-05-24 Lane 4 carve-out)
- `feedback_hint_narrative_no_time_or_location` — Maya-voice rules for tip / quest-card text

### Engine primitives

- `<<Speech>>` macro — dialog block (TLS analog: `dialog` block type with `npcId` + `content`)
- `<<linkreplace>>` cascade — TLS `cascade` block type with `props.beats` (shipped 2026-05-06)
- `thought_bubble` block type — TLS analog of RTS Speech-thought macro (shipped 2026-05-06)

---

**End of file.** Next: `doctrine/06_design_brief_template.md` for R7 brief template.
