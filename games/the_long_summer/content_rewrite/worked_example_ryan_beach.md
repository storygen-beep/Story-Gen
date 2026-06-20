# Worked Example — `ryan_beach` Before & After

> **Read this before doing any other Tier A canvas.**
> The point: see exactly what "rewritten to Prologue quality" looks like at the canvas level, and which `standards.md` rule each change embodies.

## Why ryan_beach was the worked example

It's the worst illustration of every TLS canvas pathology in one place:

- The Ryan Crack — the emotional payoff of an entire NPC arc
- 75 words total in the prior version
- Three "Yes / Not yet / No" choice labels (the canonical Yes/No-skin anti-pattern)
- Ryan's "one complete sentence" sitting alone with no setup to land it
- `@npc_ryan` token leaking into paragraph content
- Single-sentence "On the sand they cross the line they have been crossing in increments" doing the work of a full sex scene

If we can fix this scene, we have the pattern for the other 7 Tier A scenes.

---

## Before — the original 75-word canvas

```toml
[[canvases]]
id = "ryan_beach"
name = "The Beach"
description = "Week 7 Sunday. Lake an hour east. Stay with me."

[canvases.trigger]
location = "loc_beach"
npc = "npc_ryan"
is_repeatable = false
priority = 10
is_active = true
conditions = { version = "1.0", items = [...] }

[[canvases.nodes]]
id = "ride"
name = "Truck Ride"
blocks = [
  { type = "paragraph", content = "Truck ride out. Quiet. @npc_ryan has one hand on the wheel, the other on the gearshift." },
]
exit_block = { type = "choices", choices = [ { text = "Arrive.", targetType = "node", nodeId = "ryan_beach.sand" } ] }

[[canvases.nodes]]
id = "sand"
name = "The Sand"
blocks = [
  { type = "image", props = { file = "story/ryan_beach.jpg", search_queries = [...] } },
  { type = "paragraph", content = "Small sandy stretch. No one else. They swim. On the sand they cross the line they have been crossing in increments." },
  { type = "paragraph", content = "@npc_ryan says one complete sentence." },
  { type = "dialog", content = "Stay with me.", props = { speaker = "npc", npcId = "npc_ryan" } },
]
exit_block = { type = "choices", choices = [
  { text = "Yes.", ... },
  { text = "Not yet.", ... },
  { text = "No.", ... },
] }
```

**Problems present in this version (every canvas pathology in 35 lines):**

1. **`@npc_ryan` token leaking into paragraph content** (rule 23 violation). This is template scaffolding sitting in finished prose.
2. **75 total words for the Ryan Crack** — a Tier A scene at Tier F density. No setup for the proposal sentence to land. Ingold's setup-first principle: the weight of "Stay with me" comes from the five sentences that should have preceded it. Here, no setup exists.
3. **Single-sentence "they cross the line"** doing the work of an entire sex scene. The reader infers everything; nothing is dramatized.
4. **Yes/Not yet/No choice labels** — the canonical anti-pattern. Three volume dials on the same Maya, not three different Mayas (rule 12 violation, Dias).
5. **No corruption-band register** — Maya at Operating-band corruption (post-big_deal_closed) should narrate this scene with deliberate, possessive language; the prior version has no register.
6. **Ryan's voice not shown** — the design says Ryan speaks in fragments and the Beach is his ONE complete sentence (his Crack tell). The prior version says "Ryan says one complete sentence" — which is the *meta-description* of his voice, not the voice itself doing work.
7. **Smell absent** — Failbetter rule plus design book rule "smell every ~500 words." Zero in the original.
8. **Body before emotion missing** — no physical staging. We don't know where the proposal happens (sitting? lying? after sex? before?). Body has to do the meaning-making in this scene specifically.
9. **No Maya interior** — the entire Crack arc payoff has zero Maya FID. We don't see her thinking the moment.
10. **Single image, no video, generic search query** — the sex beat that's supposed to be the line-crossing has no media authoring at all.

---

## After — the 5-sub-node Option B mini-arc

See the live edit at `2_story_canvases.toml:1044-...`. Total ~1,900 words, 5 sub-nodes, 1 image + 1 video + 2 more images, story-arc node unchanged.

### Sub-node structure

| # | Node id | What happens | Rough words | Choice |
|---|---|---|---|---|
| 1 | `ride_east` | The drive. Maya in the truck cab. Sunday morning week 7, after the farmer. Quiet ride. Setup: no one has named what happened Saturday. | ~360 | "Watch the road." → lake_arrival |
| 2 | `lake_arrival` | They arrive. Park, walk to the sand, undress. They swim. Body register opens. | ~360 | "Out of the water. Toward the towel." → line_crossing |
| 3 | `line_crossing` | On the towel. Maya kisses him. The line they've been crossing in increments. Sex (Maya is the one tracking). Aftermath: she has not cried. | ~440 | "Sit up." → the_ask |
| 4 | `the_ask` | They sit up, dress, share the thermos. Ryan looks at the lake. He says her name. He says one complete sentence. *Stay with me.* She doesn't answer in this node. | ~330 | "Answer." → the_answer |
| 5 | `the_answer` | Three character-action labels, three Mayas. Effects/flagEffects unchanged from original (preserve the flag graph). | ~110 (intro prose) + choice labels | three branching → trigger return |

### Story-arc impact

`4_story_arc.toml` **unchanged.** The single existing `node_ryan_beach` story-arc node (linked_canvas = "ryan_beach", linked_flag = "ryan_beach_proposal", milestone = true) still represents the canvas-level milestone. The internal sub-nodes don't each warrant a journal entry. This is the Option B convention: **canvas-internal multi-node, story-arc-level single-milestone, unless a sub-beat is itself a story milestone deserving its own journal entry.**

---

## Rule-by-rule compliance audit

### Hygiene rules

| Rule | How the rewrite complies |
|---|---|
| **Rule 23 — Strip `@npc_xxx` tokens.** | Every `@npc_ryan` in paragraph/dialog content replaced with "Ryan" or appropriate pronoun. Tokens remain only in `npcId` props (allowed). |
| **Rule 24 — Author media blocks.** | 4 image blocks + 1 video block across 5 sub-nodes. Each has `file`, `description`, ≥3 `search_queries`. Files don't exist on disk yet; that's the next pipeline. |
| **Rule 25 — Validate after every canvas.** | Will be checked next via `package_from_toml --dry-run`. |

### Voice & POV rules

| Rule | How the rewrite complies |
|---|---|
| **Rule 6 — Free indirect discourse.** | Maya's interior carried through narrator vocabulary, never "she thought." Example (line_crossing N3): *"She felt the knowledge happen — the small clean register of: I am the one doing this; this is a thing I am choosing to do; the choice is one I have made before in the back office on Saturday and the choosing is becoming a thing I know how to do."* The italicized text is FID inside narration, not a thought-bubble. |
| **Rule 7 — Per-NPC voice.** | Ryan's only spoken lines are *"Maya."* and *"Stay with me."* in the_ask. Both fragments. The complete-sentence rule is honored — *Stay with me* is a complete sentence and it's the ONLY one in the scene from him, per his style sheet's reservation of complete sentences for the Beach Crack. |
| **Rule 8 — Body before emotion.** | We never say "Maya was anxious" or "she was moved." Body carries it: *"She felt the sentence land in her chest first and then in her throat."* Position carries it: *"His knees were drawn up. His forearms were on his knees."* |

### Specificity & sensory

| Rule | How the rewrite complies |
|---|---|
| **Rule 9 — Specific nouns.** | "the cardboard pine air-freshener that had been hanging off the rearview mirror longer than Ryan had owned the truck" — not just "the air freshener." "The small pink scar on the second knuckle of his ring finger that she had drawn once from the porch without him noticing" — specific knuckle, specific drawing memory. |
| **Rule 10 — Smell every ~500 words.** | ride_east opens with truck-cab smell (gasoline, pine air-freshener, hot vinyl, dashboard at 7am). lake_arrival has the algae warmth + wet sand + summer-lake smell. Both are inhabited (Maya breathes them in) not decorative. |
| **Rule 21 — One corruption noticing per scene.** | line_crossing carries it: *"Maya was the one who reached for the tie at the back of her top. She knew that she was the one. She felt the knowledge happen..."* This is Operating-band Maya naming her own agency in a way Closed-band Maya could not have. Distributed self-recognition. |

### Choice text

| Rule | How the rewrite complies |
|---|---|
| **Rule 11 — Real consequences per option.** | Effects differentiated: *Take his hand* gives ryan.love +20 + corruption +1; *Watch the lake* gives calculation +1 (she's deciding to delay deliberately); *Pull her shirt back on* gives ryan.love -10 + corruption +1. No two options identical. |
| **Rule 12 — The set does character work.** | Three different Mayas: the one who can take a hand and say *Stay*; the one who knows enough about August to delay without closing; the one whose body shuts the conversation before her mouth can. The labels themselves tell the story. |
| **Rule 13 — Clear in-character action.** | Each label is an action verb + concrete outcome. *Take his hand. "Stay."* is body + word. *Watch the lake. "Ask me again in August."* is gaze-direction + spoken delay. *Pull her shirt back on. Don't say his name.* is two body-actions, no words. |
| **Rule 15 — Tone, not consequence.** | None of the labels says "+rep_road" or "[+love]" — the consequences are felt through the action. |
| **Rule 16 — 3 choices.** | Three. The right number for a tonal triangle. |

### Structure

| Rule | How the rewrite complies |
|---|---|
| **Rule 1 — Failbetter density at the right tier.** | Tier A target 1500-2500 words. This canvas: ~1900. ✅ |
| **Rule 2 — Setup-first.** | The proposal sentence (the_ask N4) is preceded by ~1300 words of setup across the truck ride, the swim, and the line-crossing. The weight of *Stay with me* comes from those preceding sentences, per Ingold. |
| **Rule 3 — Get in late, leave early.** | The canvas opens at 6:45am pickup at the driveway (in late — we don't see the conversation Saturday night that led to it) and exits 240 minutes after the answer (Maya's drive home is implied, not narrated). |
| **Rule 4 — One scene = one decision.** | Five sub-nodes, but only one branches (the_answer). Each prior sub-node has a single forward choice — they're scene-pacing beats, not decisions. The single decision lands at the tier-target weight. |

---

## What did NOT change

- **Story-arc node** — `node_ryan_beach` in `4_story_arc.toml` is unchanged. The journal entry "He said one whole sentence. I gave him an answer." still applies and reads as if written for the new structure.
- **Flag graph** — All five output flags (`ryan_beach_proposal`, `ryan_keep_route`, `ryan_keep_yes_engaged` / `ryan_keep_not_yet` / `ryan_keep_no_withdrawn`, `ryan_q3_done`, `ryan_arc_complete`) preserved exactly. The downstream Keep-route canvases still receive the same gating signals.
- **Trigger conditions** — `ryan_big_deal_closed = true` unchanged.
- **Time progression** — distributed across sub-nodes (60 + 60 + 90 + 5 + 240 = 455 min) instead of single 480 min on the answer. Net player-clock impact is similar.
- **Stat effects on Yes/No branches** — `npc_ryan.love +20` on yes, `−10` on no, preserved. Added small `corruption +1` on yes and no (the act happened either way). `calculation +1` added on Not Yet (Maya is being strategic).

---

## What this teaches you about the other 7 Tier A scenes

When you do `frank_catch_living_room`, `frank_crack`, `frank_call_out`, `jake_peek_discovery`, `jake_caught_and_hand`, `brothers_discover`, `keep_tier_fork`:

1. **Sub-node structure is justified by the beat-list in `final_book.md`.** The Phase-4 beat specs already enumerate 3-5 micro-beats per scene. Use them as your sub-node skeleton.
2. **The NPC's signature voice tell is the spine.** Ryan's complete-sentence reservation IS the Beach Crack. Frank's contraction-drop + grammar-break IS the Crack. Jake's silence IS the Caught beat. Find the spine and write around it.
3. **Setup carries the weight.** The Ingold rule. Don't compress the setup to make room for the payoff — expand the setup so the payoff lands.
4. **Maya's corruption band determines the narrator.** Reference `corruption_band_register.md`. Operating-band Maya at the Beach is different from Saturated-band Maya at the Keep-Tier Fork. The narrator changes.
5. **Choice labels = character actions, not answers.** The three different Mayas pattern (Dias). For multi-route Keep group choices (Frank's 4 routes, Jake's 4 routes), four different Mayas.
6. **Preserve the flag graph by default.** Read every existing flagEffect; preserve unless documented broken. Add stat effects sparingly and document why in the canvas comment.
7. **Story-arc nodes change only if you add a milestone-deserving sub-beat.** Default: keep the existing single story-arc entry; sub-nodes are canvas-internal.
