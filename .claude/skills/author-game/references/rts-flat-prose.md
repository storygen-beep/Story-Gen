# RTS-flat prose — the mechanical register rules

Read this before you write any scene body — the `paragraph` / `dialog` / `cascade` blocks inside a
canvas. (For the `cascade` block's buildable shape + the **cascade-last** ordering rule — a `cascade` must be a
node's last content block, or trailing prose renders below the reveal link — see `references/engine-reference.md`,
the cascade section.) It is the **HOW** of register: the three axes, the nine numbered rules, the tiers, and the
pre-emit checklist. The **WHY** (density of decision-pressure over density of prose, the
throttle/odometer model) lives in `references/rts-design-philosophy.md` — don't re-derive it here.

**RTS-flat is not "few words." It is three things, and only the first is about length:**

1. **Few words PER CLICK.** ~35–40 words per beat — **flat across every tier**. You escalate a scene by
   adding *beats*, not by fattening paragraphs.
2. **SPOKEN, not narrated.** RTS runs **0.73 narration words : 1 dialogue word** — more dialogue than
   narration, including in its sex scenes. Every game this skill has shipped runs 5:1 to 19:1 the other
   way. **This is the drift.**
3. **The BODY, not the room.** RTS writes body sensation constantly and paints a room almost never.
   "Zero sensory detail" was always half-wrong.

**The contract is "specificity, not literary density."** Specific ("the runner Diana picked out") without
being literary (no extended metaphor, no narrator-supplied backstory). This is adult content: at sexual
register be direct and crude with real anatomical terms — the flat rules govern *shape*, never *whether
the content is explicit*. And it isn't only a house preference — §1E records the same economy at the top
of the market.

**And "specific" serves "hot."** These are shape rules for a **porn game**: the player is the erotic subject
and the prose exists to **arouse** them. Flat is how the writing stays re-readable and crude — never a
licence to write a cold literary thriller that merely contains sex. **Rule 9 owns that target; the other
eight serve it.**

> **When in doubt: fewer words per beat, and MORE beats.** (The old advice — "fewer words *and* fewer
> beats" — was wrong on the second half, and it is what produced our three-beat capstones.)

**Every number in this file is measured, not asserted.** See §1.

## Contents
- §1 — The measured shape of RTS (ground truth)
- §2 — Register is THREE axes: person · density · mode
- §3 — The 9 mechanical prose rules
- §4 — Choice-label discipline
- §5 — The three tiers = three beat counts
- §6 — Canvas budget = beats × 35–40
- §7 — The pre-emit checklist (run it; don't eyeball it)
- §8 — Worked examples
- §9 — The `thought_bubble` primitive
- §10 — Cross-links (don't restate)

---

## §1 — The measured shape of RTS (ground truth — cite these, don't re-derive)

Measured against the Road to Success SugarCube source
(`game_explorations/road_to_success/archive/2026-06-02T18-27-18-582Z/passage_catalog.json` — 364
passages, 273 prose-bearing). Narration = `<h3>` bodies · dialogue = `<<Speech>>` macros · a **beat** =
one revealed screen (the opening screen, plus each `<<linkreplace>>`).

### A. Tier scales BEAT COUNT. Per-beat density is FLAT.

| beats | n | median scene words | **median words per beat** |
|---|---|---|---|
| **1** (no cascade — Tier-1) | 97 | 15 | **15** |
| **2–4** | 45 | 65 | **27** |
| **5–9** (Tier-2) | 37 | 270 | **35** |
| **10+** (Tier-3) | 94 | 552 | **38** |

Read the right-hand column twice. **An RTS Tier-3 peak is not denser per beat than a Tier-2 ambient — it
has 3–4× more beats.** Its largest scene is **24 beats of ~25 words**. The old doctrine implied Tier-3
meant *richer prose per screen*. That is wrong, and it is the direct cause of our 60–90-word beats and
our three-beat capstones.

> **This maps 1:1 onto our engine.** A cascade's `beats[0]` renders on entry with the node's lead blocks
> and costs no click; each subsequent entry is one click. So **`len(props.beats)` == the RTS beat
> count**, and *visible clicks = beats − 1*. Beat 0's budget covers the node lead **plus** `beats[0]`.

### B. RTS is DIALOGUE-DOMINANT. We are not — in any game we have ever shipped.

Whole corpus: **0.73 narration : 1 dialogue.** Its *deepest* cascades are its most dialogue-heavy
(`PriestVisit`, 19 beats → **0.40 : 1**).

| game | narration : dialogue |
|---|---|
| **Road to Success — the target** | **0.73 : 1** |
| `last_call` (our best) | 5.77 : 1 |
| `the_inheritance` | 5.79 : 1 |
| `vesper` | 7.25 : 1 |
| `late_shifts` | 15.04 : 1 |
| `mothers_place` | 19.34 : 1 |

Our *block lengths* are roughly right. Our **mode is backwards, in every game, without exception.** See
Rule 4. This is the single most important number in this file.

### C. Body: written constantly. Room: almost never — and only on the location card.
25 environmental lines across 364 passages, and the room-painting ones are all **location cards**, never
scene bodies. Body sensation runs to 127 narration lines. See Rule 3.

### D. Labels are two populations, and it isn't close.
**686 nav/menu buttons: 74% carry emoji, median 2 words.** **1,559 in-cascade beat labels: 4% carry
emoji, median 4 words.** See §4.

### E. A SECOND evidence class — the field, not RTS.
§1A–D are one corpus measured deeply (n = 1 game, 364 passages). This is different evidence, labelled so
you don't confuse them, and unlike A–D it is **not re-derivable from inside the skill** — it's a field
observation recorded here so the register rule has a market anchor rather than only a house one.

A 2026-07 study of the 30 most-engaged Twine sandboxes on mopoga (read by story, systems, and ~11k player
comments) found the same economy at the top of the market. One of the set's most-played real-porn
sandboxes runs a **median ~36 words per passage** (400 sampled) across **~3,700 passages**, and its players
call it addictive with zero grind complaints in 704 comments. Nothing in the top tier reads as literary —
one winner markets the point outright ("ditches tedious walls of text"), and others simply practise it
(prose as connective tissue between images; 1–3-sentence hubs). Text-only games survive up there **only**
when a simulation replaces the media, and even the best of those has "needs pictures" as its top complaint.

**So: literary pressure on Lane 1/2/3 prose is a regression, not an improvement** — those beats repeat, and
density that reads well once reads as performance by the third pass (§2). See Rule 2 and §5.

---

## §2 — Register is THREE axes: person · density · mode

**This file owns all three.** `references/lanes.md` "Voice register" says which *value* each lane takes;
`SKILL.md` and `references/beat-authoring.md` cite them. Nothing else defines them.

| axis | values | scope | declared at | audited by |
|---|---|---|---|---|
| **person** | `second` (default) · `first` · `third` | **the whole game** — one value, **immutable** after the seed | Step 0+1 → `design_book.md` "World setup" + `authoring_state.json` `register.person` | Rule 1 · §7 check 1 |
| **density** | RTS-flat (Lane 1/2/3) · Tier-3 earned (Lane 4) | per canvas | the canvas's lane | Rule 2 · §7 check 2 |
| **mode** | dialogue-dominant wherever an NPC is present; narrated only when no one is there to speak | per beat | who is in the room | Rule 4 · §7 check 3 |

**Density is a dial you can miss by 1.5×. Mode is a switch you can have flipped backwards for a whole
game — and we have, in every game we have shipped (§1B). Person is a constant you can be inconsistent
about inside a single file — and we have (`late_shifts`, Rule 1).**

### Density follows the lane

| Lane | Density | Why |
|---|---|---|
| **1 — Hub buttons** | RTS-flat | Clicked repeatedly across the arc. Re-readable. |
| **2 — Ambient encounters** | RTS-flat | Fires 10–20 times across an arc. |
| **3 — Dispatcher walk-ins** | RTS-flat | Dice-rolled inside a chore. Re-readable. |
| **4 — Capstones** | **Tier-3 earned** | Once-only milestone. The single read justifies the spend. |

But note what Tier-3 now *means*: **more beats, not thicker beats** (§1A, §5). A Lane 2 ambient authored
at capstone density costs that density on **every** re-read, and by the third pass the language reads as
performative. A capstone fires once — it can afford **twelve beats**. It still cannot afford 90-word ones.

**Rarity is its own punch — escalate a scarce beat by WEIGHT, not FREQUENCY.** When a beat lands *because*
it's rare (a once-only gut-punch, an involuntary crack, a glitch peak), resist giving it a
recurring/ambient version — recurrence dilutes the scarcity that was the whole effect. The rising-frequency
saturation curve (`lanes.md` Lane 2/3) is for **repeatable ambients**; it does NOT apply to a scripted rare
beat. Make the *next* one hit harder, don't make it happen more often. (Cf. `kink-ceilings.md` —
repetition erodes intensity.)

---

## §3 — The 9 mechanical prose rules

Every Lane 1/2/3 scene body satisfies all 9. (Lane 4 capstones relax Rules 3/5/7 — see §5 Tier-3.
**Rules 1, 2, 4 and 9 never relax.**)

### Rule 1 — Write in the game's DECLARED person

Person is a **per-game constant, declared once, never mixed.** Chosen at Step 0+1
(`references/step-0-1-seed.md`), written into `design_book.md` ("World setup → Register"), recorded in
`authoring_state.json` as **`register.person`** — one of `"second"` (default) · `"first"` · `"third"`.
After the seed it is **immutable**: a person swap is a full-corpus rewrite, and on a shipped game it
rewrites prose players have already read.

- **`second` — "You take the stool."** RTS's person and this skill's **default**. The player is "you";
  the NPC is "he" / "Frank" / "him". Pick it unless the game has a stated reason not to.
- **`first` — "I take the stool."** A confessional / diary-voiced protagonist.
- **`third` — "She takes the stool."** A protagonist the player *watches* rather than *inhabits* — the
  still-point / owned-weapon PC (`vesper`). It costs you second-person immediacy — and immediacy is what
  makes the aroused body *the player's own*, so third person **cools the porn**: the player spectates
  someone else's heat instead of being the subject of their own (Rule 9). Buy it deliberately, and only for a
  story-first dark game where that cooling is the point.

**Whatever is declared, EVERY `paragraph` and `thought_bubble` block in the game is in it.** `dialog`
blocks are exempt — a speaker says "you" to the person in front of them regardless of the narration.

> Declared `second`: ✓ You take the stool. He slides a coffee across without looking up.
> Declared `third`:  ✓ She takes the stool. He slides a coffee across without looking up.
> ✗ **Both, in one game.** `late_shifts` ships *"Hank behind the counter. He looks up when **you** come in
>   from the floor."* and *"**She**'d lost the habit of knowing what time it was."* — **in the same file**.
>   362 of its 398 paragraphs narrate in third; the rest address "you". Nobody chose that; nobody noticed.
>   No build gate can see it. §7 check 1 catches it in one grep.

**"Person" is NOT "POV."** In this skill **POV** already means the protagonist's **gender** (female PC /
male PC — `step-0-1-seed.md` Step 0). The grammatical axis is **`register.person`**. Never write "POV"
when you mean person.

### Rule 2 — The beat is the unit: 35–40 words, 2 sentences of stage direction

A **beat** is one click that reveals new content. In TOML: the node's lead `blocks` merged with cascade
`beats[0]` (that's beat 0 — it costs no click), or any subsequent `beats[]` entry, or a standalone
`paragraph`/`dialog` in a one-screen canvas.

**A beat carries ~35–40 words of prose.** This is the hardest number in the file, and it is **flat across
every tier** (§1A) — RTS's 5–9-beat ambients and its 10+-beat peaks both sit at 35–38 median words per
beat. A Tier-1 one-liner is ~15.

Stage direction within a beat caps at **2 sentences**. After two, drop a `dialog` block or break to the
next beat.
> ✓ You bend to load the dishwasher. He's at the counter, mug raised. *(2 sentences, 14 words. Break.)*
> ✗ four sentences of business + window light + the kettle clicking, no dialog break

**A beat over ~50 words is a beat that wanted to be two beats.** The fix for a fat beat is **a click**,
not a shorter sentence — split it; never compress it into obscurity. (Vesper's cascades run a ~58-word
median per beat, ~1.5× RTS. Every one of them is a split away from correct.)

### Rule 3 — The BODY is mandatory. The ROOM is banned outside the location card.

The old rule ("zero environmental sensory detail") collapsed two different things and got one of them
backwards.

**BODY sensation — write it, constantly.** RTS does. It is how flat prose carries what the HUD cannot:
what this costs her, or what it does to her.
> ✓ *"Heat flares in your belly as you watch them through the cracked door… your own breathing getting
>   ragged."* — RTS, `PeepBrotherSex`
> ✓ *"You're down on your knees, doing what he wants, and your stomach is churning."* — RTS, `SecretarySex`

Body sensation encodes **RELUCTANCE exactly as readily as arousal** — a churning stomach, a burning face,
a throat that won't work, knees that won't hold. That is the flat register's entire emotional bandwidth,
and it is *cheap*: one clause, no metaphor, no interiority. **A hot beat with no body in it is
under-written, not disciplined.**

**ROOM description — banned in a scene body.** No smell of the kitchen, no window light, no dust motes,
no kettle clicking. The HUD carries location + time + NPC heat continuously; prose that paints the room
re-buys grounding the HUD already gives you, and pays for it on **every re-read**.
> ✗ The kitchen smells of coffee and damp wood. Sun catches the dust over the sink. You pour him coffee.
> ✓ You pour him coffee. He sets the paper down.

**The room gets exactly one home: the LOCATION CARD.** RTS paints a place *once*, in the location's own
entry blurb, with a fixed ~25-word formula — and then **never again in any scene at that location**:
> *"You are in a church. The air is thick with the smell of incense and candles. The sound of music and
>   prayer fills the room."* — RTS, `Church`
> (`DarkAlley`, `StripClub`, `Pharmacy` are the same formula with the nouns swapped: *You are in a X. The
>   air is thick with the smell of Y. The sound of Z fills the room.*)

Write that once per location, in the location's `description` (`references/location-design.md`). Scene
bodies at that location never describe it again.

**One exception inside a body: a sensory detail that is a GATE SIGNAL.** *"As you approach the bathroom
door, you hear the shower running"* is not atmosphere — it is the fact the beat turns on: *someone is in
there.* **The test:** if cutting the sentence costs the player information the choice depends on, keep it.
If cutting it costs only *mood*, cut it.

### Rule 4 — SPEAK it; don't narrate it. Dialogue outweighs narration.

**This is the axis this skill has been failing, in every game, from the start.**

RTS's whole corpus runs **0.73 narration words : 1 dialogue word** — there is *more dialogue than
narration* in Road to Success, and its deepest, hottest cascades are the most dialogue-dominant of all
(`PriestVisit`, 19 beats → **0.40 : 1**). Ours run the other way: `vesper` **7.25 : 1**, `the_inheritance`
**5.79 : 1**, `late_shifts` **15.04 : 1**. Block length was never the problem. **We NARRATE where RTS
SPEAKS.**

> **The target — and it is a gate, not a vibe:**
> - Any scene with a **present NPC**: **narration : dialogue ≤ 1.5 : 1**. Above **3 : 1** is a **FAIL** —
>   rewrite before you ship it.
> - **Whole game: ≤ 2 : 1.** (RTS's 0.73:1 is the north star; 1.5–2:1 is the tolerance for our more
>   paragraph-forward engine. There is no version of this where 7:1 is acceptable.)
> - Run it: §7 check 3.

**Passing this makes the prose SPOKEN, not HOT.** The ratio is necessary, not sufficient — a noir author
hits ≤1.5:1 with clipped hardboiled exchanges and still writes nothing arousing. Dialogue-dominance is the
*shape*; whether the scene turns the player on is **Rule 9** (audited separately, §7 check 7). Don't read a
green ratio as a hot scene.

**The move is mechanical.** Find every narrated sentence that *reports* what a character said, felt at
someone, or decided at someone — and hand it to them as a line.
> ✗ "She asks how long he's worked here; he says four years and changes the subject."
> ✓ [You] "How long you been on this?" / [Mercer] "Four years. Coffee's cold."
>   *(same beat, half the words, twice the character)*

**Lean HARDEST at the hot beats.** A capstone, a sex scene, or a confrontation narrated as summary is the
worst drift there is — those are the beats the player waited for. **Play them; don't report them.**
Multi-party beats give each present NPC a line: short volleys, no monologues.

**EXEMPT only when no one is there to speak:** solo activities; unseen voyeur/peek beats (RTS's
`PeepBrotherSex` is 100% narration *because she is alone behind a door* — that is the exemption working,
not a counterexample); and the interior stretches of a capstone. **A present NPC is never exempt.** A mood
glimpse is one terse spoken line, not a narrated paragraph about his mood.

See §8.3 for the exhibit: a complete named-NPC introduction in **68 words — 15 narrated, 53 spoken.**

### Rule 5 — No narrator-inferred backstory

Surface only: the player gets exactly the observation the character gets. No narrator-supplied history
behind an object or a gesture — no "the cup he keeps for you," no "the chair he added when you moved in."
That is **inference the narrator has no right to** at Lane 1/2/3; it is a Tier-3 move, earned **once** at
a capstone (§5), and on the fifth re-read of an ambient it reads as performative — you cannot keep
noticing the cup thirty times.

> ✓ He pours you a coffee.
> ✗ He pours you a coffee — the same mug you'd reached for on day three, the chipped one he never tossed.
>
> *(Examples are in the DEFAULT person, `second`. Rewrite them into whatever this game declared — Rule 1.)*

**This is NOT a ban on interiority.** The PC's own body and her own snap read are *in-scene*, not
inference: Rule 3 **requires** the body, and a one-clause thought is hers, not the narrator's dossier —
> ✓ *"I should get out of here, someone could arrive at any moment."* — RTS, `PeepBrotherSex`

The ban is on **the narrator knowing things the character doesn't.**

**Also banned, as a smuggled form: the impersonal-"you" analogy simile** — *"he strips her the way you'd
tear the wrap off stock," "he looks at her the way you'd note a gauge reading."* That is narrator
inference wearing a second-person coat. It is all over `vesper`. Cut it.

### Rule 6 — Direct/crude diction at sexual register

Crude is the default at the sexual register. "His cock." "Your cunt." "Your tits." "Your ass." Not "his
manhood," not "between your legs," not "your chest." Each NPC has a **per-tier vocabulary ceiling** (one
NPC goes full breeding-talk at the peak; another stays peer/school register) — declared in that NPC's
design brief, designed at `references/content-framework.md` §F ("Their voice and their ceiling"). Default
to the maximum-explicit reading when ambiguous; the ceiling caps how far, the rule says don't soft-pedal
*below* it.
> ✓ [Frank] "Open your mouth." / You go down on your knees. His cock against your face.
> ✗ His voice was low as he asked her closer. She felt herself responding, alive with something unnamed.

### Rule 7 — One beat = one click

Each click in a cascade reveals ONE narrative beat — one paragraph, or one dialog exchange, or one
image+caption. Don't pack multi-paragraph internal momentum into a single beat; the click pacing IS the
narrative pacing, and each click is a possible stat-tick moment.
> ✓ Beat 0 "He's at the counter. He looks up." → [click] Beat 1 "He sets the mug down. Quiet." → [click]
>   Beat 2 "He crosses the kitchen toward you."
> ✗ One click: "He's at the counter, looks up, sets the mug down, says 'Quiet,' crosses, takes your wrist."

**Corollary — escalation is a beat-count operation.** To make a scene bigger, add beats. To make a moment
land harder, add beats. Never widen a beat past ~50 words (Rule 2). RTS's biggest scene is 24 beats of
~25 words. Vesper's biggest is 8 beats of ~61.

### Rule 8 — Image-first composition

The visual asset carries the scene; the prose is the ~35–40-word beat that **pins what is happening** —
not a description that repaints the image in words. This holds **even when the image is a Phase-1
placeholder**: do NOT compensate for a missing visual with more prose (that's literary drift in disguise —
the placeholder IS the missing-image signal).

> ✓ [image: scenes/kitchen_morning.jpg] / [Frank] "Coffee?" / [You] "Yeah." — the image carries the room,
>   his pose, the light; the prose pins the exchange.
> ✗ a 60-word paragraph repainting the warm light, the flannel, the two mugs, the softening face

**Image-first is WHY 35–40 words per beat is survivable.** In RTS, every cascade beat carries its own
`webp`/video — the media is what lets the beat be that short and still land. **A beat with no media is a
beat doing all its work in words, which is exactly the beat authors fatten.** If a beat has no visual, ask
whether it should.

> ⚠️ **RETIRED CLAIM — "half of RTS scenes are 25 words or less" was FALSE.** It came from a rendered-DOM
> capture that could not see `<<linkreplace>>` beats (they do not exist in the DOM until clicked), so it
> measured **beat 0** and called it the scene. True figures: **28%** of prose passages are ≤25 words, and
> those are Tier-1 one-liners; the **median RTS scene is 126 words**, and the median Tier-3 scene is
> **552**. Never cite the old number to justify a thin scene. RTS's short scenes are short because they are
> **one beat**, not because scenes are short.

The `[image: …]` above is **shorthand for this rule only** — the engine has no such syntax. Author the real
TOML media block (`{ type = "image", props = { file, description, search_queries } }`) with its
`search_queries` acquisition layer per `references/media.md`.

### Rule 9 — Write to AROUSE. The player is the erotic subject; the sex is the subject of the scene.

Rules 1–8 make prose *clean, spoken, specific.* None makes it **hot** — a game can pass all eight and read as
a cold literary thriller that happens to contain sex. (`vesper`: third person, 3.67:1, every interiority beat
about the plot. `the_inheritance`: a clean 1.47:1 and second person, yet zero explicit words and every act
skipped behind a closed door. Both pass the shape rules; both read cold.) This rule names the target the
other eight serve: **this is a porn game — the prose exists to arouse the player, and the player is the one
it happens to.**

**A. The player is the erotic SUBJECT, not a spectator.** The heat lands on *her body, her arousal, her
exposure* — the thing the player is inside of — not on a figure the player watches from outside. That is what
`second` person buys (Rule 1): the aroused body is *yours*. `third` + a still-point/owned PC spend that
immediacy on distance and make the player a **watcher** — a real cooling, legitimate only for a story-first
dark game bought on purpose (`content-framework.md` §1B). And the body Rule 3 mandates is, by default,
**desire** — arousal, want, exposure — not only reluctance, and never the plot's mood or the scene's
apparatus. In a sex scene the camera stays on the sex: her sensation, his body, the act. The instant the
words leave the bodies for the conspiracy or the machine, the scene stops being porn (`vesper`'s
drain/plate/socket lexicon is the anti-pattern — words spent on the device, not the fuck).

**B. Show the act; don't bank it and skip it.** When a beat is the sexual payoff, **put the act on the
page** — Rule 4 (play it) and Rule 6 (crude diction) say how; this makes it non-negotiable *at the payoff.* A
repeatable sex surface that shows a closed door, a one-line time-skip, and a pleasure-meter bump has **failed
the rung** — the "digital blue balls" that reads as a story with a sex-shaped hole (`sex-loop.md` `## Voice`).
Fade-to-black is a *declared ceiling* made in the open (`kink-ceilings.md` §5), never a default reflex.

**A floor, not a quota.** Something hot is always within a few actions in the ordinary hubs — the player is
never marched through long plot or grind to reach any erotic beat. This is **not** "constant sex." Two loved
shapes both pass: **ambient** (sex is the weather, a roll away — DoL) and **earned slow-burn** (the buildup is
the heat, resistance eroding over real time — Being a DIK, Karryn's Prison). What they share, and what this
protects, is that arousal lives in the **texture** the whole climb — a slow burn is still *charged*, never
dry. Protect the floor; pick the shape on purpose at Step 2.

> **Cold → hot, same act (charge, not adjectives — still RTS-flat):**
> ✗ *She goes down without a word. He takes the call one-handed, his other hand in her hair the way a man
>   rests his hand on a tool he isn't using yet.* — distant ("she"), words on the power and the simile, the
>   body a prop. Admirable; cold.
> ✓ *You go to your knees. His cock's already out — one hand fists your hair, the other lifts the phone,
>   "Yeah, I'm here," and he uses your mouth through the whole call without looking down. Your jaw aches.
>   You're wet anyway, and you hate that you are.* — second person, words on your mouth, his cock, your own
>   traitor arousal. Same beat, same crudeness budget, hot.

**Hot ≠ purple.** The hot version is *specific and crude,* not *literary and thick* (§preamble). DoL reads as
hardcore porn on flat, terse, second-person prose — the heat is the **camera** (on the body, on the act) and
the **systems** (arousal/exposure always live), not richer sentences. Adding adjectives is the wrong fix;
Rule 2 still binds. **Audited by §7 check 7.**

---

## §4 — Choice-label discipline

Labels are **two populations**, and the numbers are not close:

| | n | emoji | median words |
|---|---|---|---|
| **Nav / hub / menu buttons** | 686 | **74%** | **2** |
| **In-cascade beat labels** (`advance_text`) | 1,559 | **4%** | **4** |

- **Hub/menu button** = a **terse action verb + emoji**, ~2 words. The flavor lives in the scene the click
  opens, NOT in the label. Strip self-justifying subtext: `Square the crate 😏`, not `Square the crate. Ten
  minutes. Tell yourself it's just business.` (🔥 sex · 💬 talk · 🥃 pour · 💰 deal · ↩️ leave)
- **Cascade `advance_text`** = **bare** (no emoji), ~4 words, and it is *not* a menu verb — it is a terse
  statement of the next beat, in the declared person. RTS ships `He cums`, `Ride him`, `You get on all
  fours`, `Turn around`, `I can't do this`.
- **Crude word in the label at the ceiling.** At explicit tiers the verb is crude at the NPC's vocab
  ceiling: `Suck his cock`, not `Go down on him`.

(Full label/emoji rules: `references/lanes.md` Lane 1.)

---

## §5 — The three tiers = three BEAT COUNTS

RTS doesn't write every scene at one density. Three tiers — but **tier is beat count, not words per
beat** (§1A). Per-beat density is flat at 35–40 everywhere.

| Tier | Used for | Beats | Function |
|---|---|---|---|
| **Tier 1 — utility one-liner** | sleep / nap / generic activity-pass; Lane 1 hub menu items | **1** | pure mechanical confirmation — ~15 words, exists to make the stat-tick feel like something |
| **Tier 2 — vignette** | Lane 2 ambients, Lane 3 substitution targets, anonymous-partner encounters | **5–9** | bridges mechanic to content — specific, RTS-flat, re-readable |
| **Tier 3 — scripted character** | Lane 4 capstones; named-NPC intros, quest beats, arc transitions | **10–20** | real character writing — the layer that earns the game its narrative weight |

**RTS-flat is the Tier-1/Tier-2 default.** Budget discipline is part of why a 130-scene game ships at all
— **don't spend Tier-3 beats on a Tier-1 moment.**

**Tier-3 is EARNED, capstone-only.** What Tier-3 earns that Lane 1/2/3 forbids:
- **Interior monologue + observation tied to memory** — the cumulative weight of past arc beats lands.
- **Inferential character work** — the Rule-5 ban lifts here, *once*.
- **Composed rhythm across beats** — Rule 7's one-beat-per-click relaxes to let momentum run.

What Tier-3 is **NOT**: not thicker beats (§1A — RTS's Tier-3 runs 38 words/beat, same as its Tier-2);
not generic literary prose (it's specific to *this* scene's people); not melodramatic (the weight is in
the line, not underlined around it).

**The two drifts, both real:**
- **Tier-3 voice in a Lane 2/3 body** — capstone register leaked into a repeatable. Grates on re-read.
  *The common one.*
- **A capstone written at Lane-2 depth** — a once-only scene given 3 beats and flat prose. Wastes the
  canvas. *Ours: a capstone under 10 beats is a Tier-2 wearing a badge.*

---

## §6 — Canvas word budget = beats × 35–40. Never a flat cap.

**Do not carry a per-canvas word cap.** The retired `prompts_v2` doctrine had "Lane 1 ≤200 / Lane 2 ≤100 /
Lane 3 ≤150 words per canvas." Measured against real RTS, the **Lane 2 cap is 2.6× tighter than RTS's own
ambients** (median 270 words). Worse, a flat cap forces exactly the wrong fix: it makes you **compress the
beat** when the honest fix is **cut a beat**.

**Derive it instead:**
1. Pick the tier → that gives the **beat count** (§5).
2. × **35–40 words per beat** (Rule 2).
3. That's the budget. If the scene wants more words, it wants **more beats** — go back to (1) and ask
   honestly whether the moment earns the higher tier.

| Canvas | Tier | Beats | Budget |
|---|---|---|---|
| Lane 1 hub base render | 1 | 1 | ~15–40 w |
| Lane 1 escalation rung | 2 | 3–6 | ~120–240 w |
| Lane 2 ambient | 2 | 5–9 | ~200–350 w |
| Lane 3 walk-in + branch | 2 | 5–9 | ~200–350 w |
| Lane 4 capstone | 3 | **10–20** | ~400–800 w |
| Named-NPC intro (`npc-intro.md`) | — | 1–5 | ~70–200 w, **dialogue-dominant** (RTS's `MeetEmma` = 68 w) |

---

## §7 — Pre-emit checklist (run these; do not eyeball them)

Run **1–3** on the beat you just wrote, before `merge_toml_phases`. Run **3** on the whole game at every
milestone build and **report the number**; run **7** at every milestone too — it is the arousal gate, and
nothing else in this list can see a cold game.

### 1 — Declared person (Rule 1)
Read `authoring_state.json` → `register.person`. For `person = "second"` (the default), list every
paragraph that narrates in third with no second-person pronoun anywhere in it:
```bash
grep -ho 'type = "paragraph".*content = "[^"]*"' games/<slug>/toml_phases/*.toml \
  | grep -Ei '\b(she|her|he|him|his)\b' | grep -Eiv '\byou\b|\byour'
```
For `person = "third"`, invert — list paragraphs that leak second person:
```bash
grep -ho 'type = "paragraph".*content = "[^"]*"' games/<slug>/toml_phases/*.toml | grep -Ei '\byou\b|\byour'
```
**Reading the output — the grep is a scanner, not a verdict.** A hit is a **FAIL** only if the pronoun
refers to **the player character**. A paragraph purely about the NPC ("He sets the mug down.") is a
legitimate hit and fine; an impersonal "the way you'd…" is a **Rule 5** violation instead. So judge the
*rate*, then read the hits.

*(The second alternative is `\byour` — **no closing `\b`** — on purpose: the old `\byour\b` missed `yours`
and `yourself`, so a clean second-person paragraph ending "…like it's **yours** now" got flagged as a
third-person leak (The Inheritance beat_0008). Don't "simplify" it to a bare `\byou` prefix: that also
matches **young** and **youth**, which measurably swallows 8 genuine third-person paragraphs in our own
corpus. `you're`/`you'll`/`you've` were never the problem — an apostrophe is already a word boundary.
Both branches carry the same pattern so they measure the same token set.)*

**Real calibration** (these exact commands, run 2026-07-14 — before the prefix fix, so the counts below
are a slight over-read of the flagged column):

| game | declared | flagged | read |
|---|---|---|---|
| `last_call` | second | **10 / 172** | clean — the hits are NPC-only paragraphs |
| `the_inheritance` (v1, now `archive/the_inheritance_v1`) | second | **12 / 364** | clean — same |
| `mothers_place` | second | **6 / 44** | clean |
| `vesper` | third | **64 / 766** leak "you" | mostly Rule-5 impersonal-"you" similes — a *different* defect, worth fixing |
| **`late_shifts`** | **(never declared)** | **362 / 398** | **BROKEN** — it is a *third*-person game that leaks second person. Nobody chose that. Nobody noticed. |

**A few percent = fine. A third of your paragraphs = you have two narrators.** If your rate looks like
Late Shifts, stop and fix it before writing another beat.

### 2 — Per-beat density (Rule 2)
List every prose block over ~45 words (280+ chars):
```bash
grep -oE 'type = "(paragraph|dialog)".*content = "[^"]{280,}"' games/<slug>/toml_phases/<file>.toml | cut -c1-70
```
Then for each cascade you just wrote, sum the words in **each `beats[]` entry** (a beat is often a `dialog`
+ a `paragraph` — the **beat**, not the block, is the unit). **>50 words in one beat → split it into two
beats.** Beat 0's budget includes the node's lead `blocks`.

> **A "word" is a `str.split()` token** — the same definition check 3's script uses, so the two checks agree.
> That means **a spaced em dash or ellipsis counts as a word**: `a set of names — I've been spoofing one` is
> **nine** tokens, not eight. Harmless in the middle of a range, and not harmless when you are authoring to a
> hard number (a band held to exactly 21, a beat sitting at 50). Count with the script, not by eye, whenever
> the budget is exact.

### 3 — Narration : dialogue (Rule 4) — THE ONE THAT MATTERS
```bash
python3 - <<'PY'
import re, glob
n = d = 0
for f in glob.glob('games/<slug>/toml_phases/*.toml'):
    if f.endswith('7_final_game.toml'): continue
    for m in re.finditer(r'type = "(paragraph|dialog)"[^\n]*?content = "((?:[^"\\]|\\.)*)"', open(f).read()):
        w = len(m.group(2).split())
        n += w if m.group(1) == 'paragraph' else 0
        d += w if m.group(1) == 'dialog'    else 0
print(f"narration {n} : dialogue {d}  =  {n/max(1,d):.2f} : 1")
print("RTS = 0.73:1 | target <= 2:1 whole-game | > 3:1 on an NPC scene = FAIL")
PY
```
**If the number is climbing, you are narrating scenes that should be played.**

### 4 — The room (Rule 3)
Did any scene body describe the location? Cut it — the location card already did. Did the hot beat contain
**no body sensation**? Add it: that's under-written, not disciplined.

### 5 — Tier = beats (§5)
Is this a capstone with fewer than **10** beats? Then it's a Tier-2 ambient wearing a capstone's badge. Is
it a Lane-2 ambient with more than **9**? Then it will grate on the third re-read.

### 6 — The two sanity questions
- *"Could this exact beat appear in an RTS scene of the same tier?"* If the honest answer is "RTS would
  never ship this — it reads like a literary novel," rewrite it flat.
- *"Would RTS have given this moment this FEW clicks?"* If no — add beats.

### 7 — Written to arouse (Rule 9) — not greppable; read it
Arousal is not a word count, so this one is a read, not a grep — run it at every milestone. Read three
ordinary (non-payoff) beats and one sex scene and ask:
- **Body or world?** Do the narration words land on the player's body / arousal / exposure, or on the room,
  the mood, the plot, the apparatus? An ordinary beat whose words are about the world is drifting to story
  (Rules 3, 9A).
- **Subject or spectator?** Is the heat happening to *the player* (second person, her body), or is she a
  third-person figure the player watches? A declared still-point/owned PC is fine *if bought on purpose*
  (Rule 1); an accidental spectator stance is the `vesper` cooling.
- **Shown or skipped?** Does every repeatable sex surface and every payoff **depict the act**, or does one
  fade to a closed door + a stat bump? A skipped act is a failed rung (Rule 9B), not restraint — unless the
  ceiling declared it (`kink-ceilings.md` §5).

The failure this catches passes checks 1–6: `the_inheritance` is clean on person, density, and mode and
still elides every act. Clean shape, no heat.

---

## §8 — Worked examples (real RTS, verbatim)

### §8.1 — Tier-1: one beat, 7 words (`BedroomStudy`)
> **STUDY**
> *[image: study.webp]*
> You studied an hour and feel smarter!

That is the entire passage. One beat. No cascade. This is what a Lane 1 activity-pass looks like.

### §8.2 — Tier-2 cascade: 5 beats, ~41 words/beat (`PeepBrotherSex`)
> **Beat 0** *(entry — 32 words)*
> You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a
> girl, their bodies tangled together... and they're definitely not just sleeping!
> *[image: brotherEvent{1-6}.webp — randomised per fire]*
>
> **Beat 1** → click `Peep` *(35 words)*
> Heat flares in your belly as you watch them through the cracked door. Your Stepbrother is groaning, his
> hands gripping the girl's hips as he moves over her. You're mesmerized, your own breathing getting ragged.
> *[video: masturbate1]*
>
> **Beat 2** → click `Stroke your pussy` *(gated `arousal > 0`; 32 words)*
> You can't help yourself. You slip your hand under your shorts, your fingers finding your already wet
> folds. The sounds of their moans and gasps fill the air, fueling your own desire.
> *[video: masturbate2]*

Three things at once. **Rule 3's body exhibit** — "Heat flares in your belly", "your own breathing getting
ragged": this is the sensory writing the old Rule 3 wrongly banned. **Rule 2's per-beat invariant** — 32,
35, 32. And **Rule 4's exemption** — it's 100% narration *because she is alone behind a door*. Nobody is
there to speak. That's the exemption working, not a counterexample.

Note also: **randomised media on a repeatable**, and a **bare, crude, in-person `advance_text`** (`Stroke
your pussy`) — §4.

### §8.3 — Mode: a whole NPC introduction in 68 words — 15 narrated, 53 spoken (`MeetEmma`)
> **WHO'S THIS GIRL?**
> *[image: emmaPlaying.webp]*
>
> [You]  "Hey, what are you playing?"
> [Emma] "Oh, hi! I'm playing a game called 'The Last of Us'. Have you heard of it?"
> [You]  "No I haven't, but it looks fun"
> [Emma] "It is! I'm Emma by the way, nice to meet you"
> [You]  "I'm @player, nice to meet you too"
> [Emma] "Do you want to play a game with me?"
> [You]  "Sure, why not"
>
> You and Emma play the game for a while, you have a great time together.
>
> `[Leave]` → unlocks Emma's talk hub

**That is the entire canvas.** Name, hook, want, tone, and an on-ramp — all carried in dialogue; one
narrated line to close the time-skip. **Now ask what this skill would have written**: two atmospheric
paragraphs *about* a girl playing a game, her posture, the light off the monitor, what her focus said
about her. That gap is Rule 4, and it is the whole reason our games read the way they do.

### §8.4 — Tier-3: MORE beats and MORE dialogue (`PriestVisit`)
19 beats · 1,072 words · **0.40 narration : 1 dialogue**. RTS's deepest scenes are its *most* spoken. A
Tier-3 capstone is not a wall of prose — it is a long, played exchange. If your capstone is 3 beats of
90-word paragraphs, you have written the inverse of a capstone.

### §8.5 — The location card: the ONE place the room lives (`Church`)
> **CHURCH**
> You are in a church. The air is thick with the smell of incense and candles. The sound of music and
> prayer fills the room.
> `[Pray]` `[Confessional]` `[Visit the priest]`

25 words, three sentences, once. Every scene at the church after this describes **zero** of it.

### §8.6 — BEFORE / AFTER: literary drift, caught in our own work

**A Lane 1 hub render** — 50 words → 10 (drift: Rule 3 room, Rule 4 mode, Rule 2 density):
> **✗ Before:** Maya pours Frank a cup of coffee, the steam rising between them. She catches the way his
> hand lingers near hers when he takes the mug, the way he meets her eyes for a moment longer than
> necessary. There's something unspoken between them that morning — a small recognition that they're both
> alive to whatever this is becoming.
>
> **✓ After:**
> *[image: scenes/kitchen_morning_pour.jpg]*
> [You]   "Coffee."
> [Frank] "Thanks, girl."

**A Lane 2 ambient** — the midnight-kitchen drift:
> **✗ Before:** The kitchen at midnight has a different quality of silence — the kind where every
> floorboard sounds like a confession. Frank is at the counter, his back to you, a glass of something
> amber in his hand. He doesn't turn when you come in. He's heard you. He waits.
>
> **✓ After:** Frank's at the counter. He doesn't turn.
> [Frank] "Late."

**The Marge case** (`28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md:262-276`) — the
one that cost eight hours. Every canvas came out as 50-word paragraphs with sensory detail and inferential
framing:
> **✗ Before:** You take the stool at the end of the counter where the napkin holder needs refilling. Marge
> slides a coffee across without asking how you take it; she's seen you take it twice now.
>
> **✓ After:**
> [Marge] "What."
> [You]   "Coffee."
> [Marge] "Two bucks."

Read those three "before" blocks again. They are *good writing*. That is exactly why this file exists —
the drift never feels like a mistake while you're doing it.

---

## §9 — The `thought_bubble` primitive

A real content block type — the private-thought glimpse. Renders as an italic bubble distinct from speech:
a 💭 glyph + "is thinking:" label, dashed border, muted color (`v2.py:13878` — `elif block_type ==
"thought_bubble"` render; player/NPC/unknown speaker variants resolve through the same path,
`v2.py:13885-13922`). It is **orthogonal to the three tiers** — it adds character interiority through a
styled UI element, NOT through prose density, so the surrounding prose stays RTS-flat.

```toml
{ type = "thought_bubble", props = { speaker = "npc", npcId = "npc_frank" }, content = "She doesn't know I watch her like this. Good." }
```

**Use it for** an NPC's charged interior on a Lane 2/3 ambient (adds his perspective without Tier-3
spillage — the bubble carries the interiority, the prose stays flat) and for the extra interiority
dimension on a Lane 4 capstone.

**Don't use it for** a Lane 1 utility menu item (one-line scene — a bubble is over-weight) or for the
player's own interior (the player's POV *is* the scene; thought-bubbles are for NPC interior — a `speaker =
"player"` variant exists in the engine but is reserved, not the default).

**It follows the declared person** (Rule 1) — a `thought_bubble` is narration, not speech.

---

## §10 — Cross-links (don't restate)

- **The WHY** — density of decision-pressure over density of prose, throttle vs odometer, the two-axis
  gate: `references/rts-design-philosophy.md` (P1–P11).
- **Which register value each LANE takes** (the lane → value lookup): `references/lanes.md` "Voice
  register". **The three axes are DEFINED here, in this file** (§2) — `lanes.md` says which value a lane
  picks, it does not define the axis. (Before 2026-07-14 the two files pointed at each other and neither
  owned the mode rule, which is exactly why it had no teeth.)
- **The per-NPC vocab ceiling** (how explicit each NPC's peak gets, the crudest word the prose will use,
  recorded in the design brief): designed at `references/content-framework.md` §F.
- **Choice-label + emoji rules in full** (hub menu vocabulary, locked-visible ladder): `references/lanes.md`
  Lane 1.
- **Where the room lives** (the location card + its ~25-word formula): `references/location-design.md`.
- **The person declaration** (the Step-0+1 gate + the ledger field): `references/step-0-1-seed.md`,
  `references/ledger-schema.md`.
- **The trait/tier data** (which stat bands the prose can be heat-framed against):
  `references/trait-catalog.md`, `references/trait-design.md`.
