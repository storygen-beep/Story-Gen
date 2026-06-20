# Choice Label Patterns — TLS

> **Mandatory read before writing any `exit_block.choices` array.**
> The most consistent failure mode in current TLS Phase 1 prose is choice-label sterility. This file is the reference.

## The core principle

> A choice label tells the player *what Maya does in character*, with a tone that distinguishes her from the other Mayas she could have been in this moment.

Two questions to ask of every label:

1. **Does the button text alone tell me what Maya is doing?** (Failbetter rule)
2. **Does the *set* of three labels make me feel like three different Mayas?** (Dias rule)

If either is no, rewrite.

## The corruption-band frames

From `final_book.md:454-459`. Use as starting framing per band; substitute the actual scene's verbs.

| Band | Choice-text framing examples |
|---|---|
| **Closed (0-24)** | *"Smile politely / Keep my eyes on my plate / Say thank you and leave."* |
| **Opening (25-49)** | *"Let him see / Hold the look a second longer / Lean against the counter."* |
| **Operating (50-74)** | *"Tilt the room / Close him / Say what he needs to hear."* |
| **Saturated (75-100)** | *"Let him choose the tier / Pick a number higher than he expected / Leave the key where she'll find it tomorrow."* |

## Anti-patterns — DON'T

### ❌ Yes/No skins

Found at TLS `ryan_beach.sand` line 1075-1077:

```toml
{ text = "Yes." ... }
{ text = "Not yet." ... }
{ text = "No." ... }
```

These are three volume dials on the same Maya. They name *the answer to the proposal* but not *what Maya does in the moment*. The player learns nothing about who she is from the labels.

**Fix:** Each label should be an action Maya takes, not an answer she gives. *"Reach for his hand. Yes." / "Watch the water. Not yet." / "Pull her shirt back on. No."*

### ❌ Generic verbs

Found across Phase 1: *"Continue," "Walk home," "Clock out," "Get out," "Inside," "Bed."*

These are mechanical transitions. The player learns nothing about Maya. Worse, the same labels recur 15+ times across canvases — choice fatigue.

**Fix:** Replace with character-revealing alternatives. *"Walk the long way" / "Straight home — she doesn't want to think" / "Cut through the back lot."* Same destination, different Maya.

### ❌ Mechanical reporting

Found at `frank_phase_a_test`: *"I forgot. Sorry, @npc_frank." / "I'll get it. (stand up)" / "It was on a timer I didn't know about."*

Two problems: (1) the `@npc_frank` token leaking, (2) the parenthetical *(stand up)* is a stage direction inside a choice — the action belongs in the resulting prose, not in the button.

**Fix:** *"I forgot. Sorry, Frank." / "I'll get it now." / "It was on a timer I didn't know about."* Strip parentheticals; let the result body show the standing.

### ❌ Confirmation-binary

*"Are you sure?"-style follow-up choices. Anything where one option is "Yes" and the other is "Cancel" or "Back."

If the player needs an "are you sure," the setup didn't do its work. Rewrite the setup, not the choice.

### ❌ Cost-only labels

*"[Spend $20]"* / *"[Lose 10 energy]"* without character framing.

**Fix:** *"Pay it. Walk past the receipt without folding it."* The cost is in the action.

## Patterns — DO

### ✅ Action + register

Three labels, three different Mayas, all leading to the same outcome (or different outcomes if the scene branches mechanically):

> *"Hold the look."*
> *"Look down."*
> *"Smile and look away."*

Each tells the player something about Maya at this moment. Same scene, three Mayas.

(Note: TLS `activity_diner_t0` *has* these labels — but with identical stat effects. The labels do character work; the mechanics betray it. Fix the mechanics.)

### ✅ Imperative + concrete object

> *"Pick the dress she hasn't worn. Rehearse the line."*
> *"A drink first. Then the dress."*
> *"Grab something. Don't think. Go."*

(From Prologue N5 — the calc_tier choice.) Each is two sentences: an action and the framing of *how* she does it. The framing is the character work.

### ✅ Quoted dialog as label

When the choice IS a line of Maya's, quote it:

> *"\"I'll come.\""*
> *"\"I need the morning to myself.\""*
> *"\"I'm not ready to decide.\""*

Three different ways of declining the same offer. Each is a Maya.

### ✅ Body-action label

When the moment is too quiet for words:

> *"Reach for his hand."*
> *"Watch the water."*
> *"Pull her shirt back on."*

(The ryan_beach answer, re-imagined.)

### ✅ Cost-revealing where diegetic

When Maya knows the cost:

> *"Pay it. Walk past the receipt without folding it."* [-$60]
> *"Tell Diana she's short."* [+rep_church but —pride]
> *"Take the Thursday."* [time after midnight, +tip access]

Mechanical bracket optional; the action carries most of it.

## Length

Per Failbetter: **≤20 words per label**. Most TLS labels should land at **3-12 words**. A 1-word label is acceptable for terse beats; a 15-word label is acceptable when the framing is the action; never go over 20.

## Worked example — fixing ryan_beach.sand choices

**Current (anti-pattern, Yes/No skin):**

```toml
exit_block = { type = "choices", choices = [
  { text = "Yes." ... },
  { text = "Not yet." ... },
  { text = "No." ... },
] }
```

**Rewrite (action + register, three different Mayas):**

```toml
exit_block = { type = "choices", choices = [
  { text = "Take his hand. \"Stay.\"" ... },              # yes — Maya picks it back to him
  { text = "Watch the lake. \"Ask me again in August.\"" ... },  # not yet — Maya holds her ground without closing the door
  { text = "Pull her shirt back on. Don't say his name." ... },  # no — body shuts the scene before the words can
] }
```

Each label tells the player exactly what Maya does. The set makes three different Mayas legible. Mechanical effects unchanged.

## Quick checklist (paste in your head before every choice block)

- [ ] Does the button text alone tell me what Maya does?
- [ ] Are the labels three different Mayas, not one Maya at three volumes?
- [ ] No `@npc_xxx` tokens in the text
- [ ] No parentheticals as stage directions
- [ ] No "Yes" / "No" / "Continue" / "Back" / "Cancel"
- [ ] ≤20 words per label
- [ ] Effects/flagEffects on each option are not all-identical (unless the choice is genuinely cosmetic and the scene needs it)
- [ ] The corruption-band framing matches the scene's gate

---

## Reading physical text — the blockquote authoring pattern (added Session 2.5)

> Scope: this is a prose-authoring note, not a choice-label rule. Lands here because it affects how setup prose precedes a choice — when Maya is reading something, the read text gets visual separation so the decision that follows has its own weight.

Per `standards.md` Rule 26: when Maya is *reading* a physical text — brochure, rent notice, ledger line, text message, handwritten sketchbook annotation — use a raw `<blockquote>...</blockquote>` inside its **own** `paragraph` block. Dialog is wrong (it's not being spoken). Plain narration is wrong (it loses the visual distinction between her mind and the thing she's reading).

### Authoring pattern

```toml
[[canvases.nodes]]
id = "base"
name = "Desk"
blocks = [
  # Narration frames the act of reading
  { type = "paragraph", content = "The brochure was folded to the page she kept open. She did not need to re-read the heading. She re-read it anyway." },

  # The read object — blockquote in its own paragraph block
  { type = "paragraph", content = "<blockquote>Millhaven Community College. Summer term applications close June 30. Tuition for in-state students: $1,500. Federal aid available.</blockquote>" },

  # Narration resumes with Maya's interior response to what she just read
  { type = "paragraph", content = "Fifteen hundred dollars. The number that had been the number since Tuesday morning when she had opened the envelope and sat on the bed with the envelope in her lap until the room got dark." },
]
```

The reader sees Maya read the text without being told *"she read it."* The blockquote does the work typographically.

### When to use

| Scene | Candidate blockquote |
|---|---|
| `activity_brochure_journal` (Tier F) | Admissions letter line (specimen above) |
| `rent_shortfall_first` (Tier C) | Frank's handwritten figure in the ledger, or the rent-notice envelope on the table |
| `the_math` (Tier B) | Maya's own calculation, laid out differently from her narration |
| `jake_caught_and_hand` (Tier A) | A line of Jake's handwriting on a sketch caption |
| Possible Diana-texture scene | A text message on Maya's phone screen |

### When NOT to use

- **Dialog** — if someone *says* the text aloud, it's a `dialog` block
- **Interior thought** — if Maya is thinking in her head, use `*italic*` inline (Rule 26 category a), not blockquote
- **Flashback narration** — if Maya is remembering a past event, tense and prose rhythm carry it; blockquote would telegraph the flashback
- **Memory-as-voice** — a Daniel-fragment surfacing mid-scene uses `*italic*` (Rule 26 category b), not blockquote

### Format rules

- **Own paragraph block.** Don't inline a blockquote inside a larger narration paragraph.
- **No nested blockquotes.** One level only.
- **Escape quote characters** inside the blockquote content if you need literal `"` in the read text (use `\"`).
- **No italic regex inside blockquote content** unless you want the `*word*` → `<em>` conversion (it runs on all paragraph content before HTML passthrough).
