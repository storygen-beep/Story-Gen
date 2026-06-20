# Style Sheet — Maya (protagonist, narrator)

> **Mandatory read before any scene with Maya as POV (which is every scene).**
> Source anchors: `final_book.md:402-489` (Maya profile + corruption-band voice evolution); Prologue `2_story_canvases.toml:71-431` (voice exemplar).

## Identity in one paragraph

Eighteen, artist-inclined, dark hair pulled back with whatever's at hand. Inherits a Prologue collapse — boyfriend Daniel cheated with best-friend Sarah; she revenge-cheated with Sarah's boyfriend Kevin. Arrives at Frank's house carrying that. Wants independence as a literal dollar amount, not a degree. Won't ask for help; pride is the engine that the math exploits. Sketchbook is her one honest register — even at Saturated corruption, sketches stay clean.

## Voice — third-person close, free indirect discourse

The narrator sits in third-person close through Maya. Borrows her vocabulary, rhythm, emotional coloring without quoting it. **Never write "she thought" or italicize a thought.** The narration *is* her thinking.

Closed band specimen (Prologue N1):
> "She had never told him she did this — lay in bed mapping the room before she opened her eyes. It felt like something she shouldn't describe out loud, the way some private rituals felt more hers the less they were said."

Opening-band specimen (Prologue N3):
> "She knew the count because later, in her apartment, she would try to reconstruct exactly how long she had stood there, and she would not be able to decide, and her inability to decide would become one of the things she carried."

## Sentence-length signature

**Mixed.** Long subordinated sentences when she's observing, processing, or cataloguing; short declarative ones when something lands. Never staccato subject-verb-object for paragraphs at a stretch — that's the failure mode of post-Prologue Phase 1 prose. The Prologue routinely braids 3-4 clauses with em-dashes and parentheticals.

Allowed: a single short sentence as a beat-landing after a long one. *"She closed the door. She closed it quietly."*

## Vocabulary range

Working-class-adjacent + art-student. Comfortable with "comma-shaped water mark," "the particular knuckle of his left ring finger," "the kind of sex that went anywhere dramatic." Avoids both lit-fic preciousness and trying-too-hard slang. Specificity over abstraction always — *"yesterday's coffee, the one she hadn't dumped"* not *"old coffee."*

## Recurring obsessions (must surface naturally across scenes)

- **Hands** — public register. Every NPC first-described passes through their hands. Carpentry hands, holding-a-cup hands, the angle of a knuckle.
- **Dicks and dreams of them** — private register. Bed-in-the-dark layer. A dream-shape lands on a specific man and she wakes annoyed at the target. Lives in solo scenes, the moment before sleep, never in public scenes.

## Corruption-band voice — the four narrators

Full reference: `corruption_band_register.md`. Quick gist:

| Band | Sentence rhythm | Internal stance | Pronoun habit |
|---|---|---|---|
| **Closed (0-24)** | Long observational; hedges | Notices being looked at as surprise. Catalogs without naming. | "she" + passive + qualifier |
| **Opening (25-49)** | Lengthens; she catches herself noticing | Patterns visible. Names a few. | "she" + "let herself" / "registered" |
| **Operating (50-74)** | Shorter, more declarative; verbs of agency | Picks targets. Names what she's doing. | active verbs replace "she" + adjective constructions |
| **Saturated (75-100)** | Minimal hedging; subject + active verb | Speaks the language she made. *Millhaven* is hers. | possessive ("my Thursday, my booth") |

## Body language tells (every scene needs one or two)

- Pulls hair back with whatever's at hand — pencil, elastic, hem of t-shirt
- Watches hands first
- Closes doors quietly even when she could slam them (Prologue calibration — *"the part of her that slammed doors had not been in the room with her, apparently, for some time"*)
- Sits on edges (bed, bench) before deciding to sit
- Maps a room with eyes closed
- Sketchbook open in the room when she's processing — does not always draw

## Voice rules — DO

- Free indirect discourse: narration borrows her voice
- Specificity of noun (the comma-shaped water mark, not the stain)
- One private noticing per scene (the corruption-arc work happens here)
- Body before emotion — show position, gesture, sensation; let interior meaning emerge
- Smell every ~500 words; load-bearing not decorative
- Art-as-honesty escape valve at high corruption (sketchbook stays clean)

## Voice rules — DON'T

- Don't narrate "Maya felt X" — show what she sees instead
- Don't italicize her thoughts
- Don't use "heart pounding," "drunk on," "electric," "every fiber" — banned per design
- Don't use AI-slop verbs: "leverage," "delve into," "navigate," "seamless," "robust"
- Don't have her *announce her own change* — distributed self-recognition is the rule
- Don't write "@npc_xxx" tokens in paragraph or dialog content (only allowed in `npcId` props)

## Choice-text framing per band

Per `final_book.md:454-459`:

- **Closed:** *"Smile politely / Keep my eyes on my plate / Say thank you and leave."*
- **Opening:** *"Let him see / Hold the look a second longer / Lean against the counter."*
- **Operating:** *"Tilt the room / Close him / Say what he needs to hear."*
- **Saturated:** *"Let him choose the tier / Pick a number higher than he expected / Leave the key where she'll find it tomorrow."*

These are *frames* not literal text — the labels reveal Maya's decision posture, not just the next-scene transition.

## Specimen lines — to internalize before writing

Closed (Prologue N1):
> "Light against the eyelids: soft, morning, the blinds half-closed the way they had been closed last night. A car going past, two stories down. The building's heating clicked and settled."

Closed→Opening pivot (Prologue N3):
> "She closed it quietly. She did not slam it. The part of her that slammed doors had not been in the room with her, apparently, for some time."

Opening (Prologue N4):
> "Item four appeared. It appeared whole. It was not a thought she constructed — it was a thought that was already there when she turned her attention to it."

Operating-tier target (write this voice for B19, ryan_beach post-deal, Frank-Crack):
> *"Thursday was the trucker shift and she wore the blue, because the blue ran two dollars more per table than the grey, and she wasn't lying to herself about why anymore."* — `final_book.md:469`

Saturated-tier target:
> *"She closed the till at eleven. The key went into her pocket. She walked the hour home by the light of other people's porches and thought about nothing, which was the thing she'd been practicing."* — `final_book.md:471`

## Inline texture — when italic earns its place (added Session 2.5)

See `standards.md` Rule 26 for the full typography doctrine. For Maya specifically, italic (`*word*` → `<em>` at render) is the only inline marker used in her prose. **Four categories; one example each. Aim for ≤1 italic span per ~400 words.**

### (a) FID-thought beats — narration names what she's doing

The narrator pulls back from the scene for a clause to let Maya's interior register the action she's inside of. Use when the corruption arc is advancing and she is *naming* the change.

Specimen (ryan_beach.line_crossing, Operating band):
> "Maya was the one who reached for the tie at the back of her top. She knew that she was the one. She felt the knowledge happen — the small clean register of: *I am the one doing this; this is a thing I am choosing to do; the choice is one I have made before in the back office on Saturday and the choosing is becoming a thing I know how to do.* The artist part of her noticed the registering and did not interrupt it."

The italic span is the FID-thought — her interior voice landing inside the narration without a "she thought." Band-matters: this lands harder at Opening and Operating bands where Maya is starting to name things. At Closed band the italic-FID would feel premature; at Saturated band she doesn't need to narrate it anymore (the register has internalized). See `corruption_band_register.md` for per-band italic cadence.

### (b) Memory intrusion — a past voice or sensation surfacing mid-scene

A Daniel-line from the Prologue surfacing mid-Frank-scene, or a flash of Kevin-from-the-upstairs-bedroom while Maya is in the diner. Use sparingly — overuse drags her out of the present.

Specimen (hypothetical, frank_catch_living_room):
> "She did not look up. She kept her hand where it was. In the back of her head Daniel's voice said *In a minute,* the way he had said it that last morning, and she heard it and put it down."

The italic carries the remembered voice without being a dialog block (he isn't speaking in this room) and without being Maya's own interior (it's a quote from elsewhere).

### (c) Textual objects she is *reading* (inline fragment form)

For short read-fragments — a sign, a t-shirt slogan, a one-line receipt note — italicize inline inside narration. For longer read objects (a brochure paragraph, a ledger entry, a letter) use the **blockquote pattern** in `choice_label_patterns.md` instead.

Specimen (Prologue N4, paraphrase structure — Maya reading the sketchbook):
> "The sketchbook was on the desk. It had been open since the weekend to a page of Daniel's hands."

In practice most read-text should be blockquoted per Rule 26. Italicized inline read-fragments are the exception — use when the fragment is <10 words and inlined narratively.

### (d) Verbal tics / signature phrases quoted inside narration without being spoken

When a Frank signature like *"that was the agreement"* surfaces in Maya's narration (she's thinking of the phrase he would say, but he isn't in the room), italicize the phrase to mark it as quoted-but-not-spoken.

Specimen (hypothetical, rent_shortfall_first):
> "She counted it twice. She put the second stack on the first stack. She put the stack in the envelope and the envelope on the table. *That was the agreement,* Frank would say on Sunday. He would not have to. She would put the envelope there an hour before he came in from the porch, and the envelope being on the table was the sentence."

The Frank-voice is quoted into Maya's interior. She isn't imagining him speaking in-scene; she's invoking his line as a *known phrase of his* that carries weight in her head.

### What NOT to italicize

- Generic emphasis (*really*, *so*, *very*) — banned
- Entire sentences because they feel important — banned (setup does this work, not italic)
- Foreign words, song titles, book titles — use if literary convention demands (rare for TLS)
- Internal thoughts where FID already carries them — the narration IS her thought; italic is redundant and breaks the FID rule

### Cadence rule

Skim your scene after writing. Count italic spans. If you have more than one per ~400 words, pick the one that lands hardest and make the others regular narration. Over-italicizing is the failure mode; under-italicizing is safer.
