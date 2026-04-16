# Activity Types — Design Reference

Reference document for designing repeatable activity canvases. Each activity in a game should follow one of these types. The type determines the structure, pacing, and choice format.

Pick the type based on **why the player is there:**
- For themselves → Solo
- For the money/work → Task
- For the NPC (casual) → Hangout
- For the NPC (deep) → Chain
- Hybrid of hangout + task → Scene

---

## Type 1: Solo

**When to use:** Player is alone. No NPC. Self-improvement.

**Structure:** One node. No choices. Do the thing, get the stat, done.

**Examples:** Yoga, jogging, shower, nap, journal, self-care, morning routine, sleep.

```
NODE: base
  Content: scene description (2-3 paragraphs)
  Exit: trigger → stat gain + time passes, done
```

**Design notes:**
- Keep it short. 2-3 paragraphs max.
- One stat gain (fitness, energy, beauty, confidence).
- No NPC interaction. No choices.
- These are time/energy sinks — the player trades time for personal stats.
- Media: one image.

**Example:**

```toml
[[canvases.nodes]]
id = "base"
name = "Yoga"
blocks = [
  { type = "paragraph", content = "Lily rolls out an imaginary mat. Stretches, breathes, tries to quiet her head. The floor creaks. Through the wall, she hears Jake's pencil stop — then start again." },
  { type = "image", props = { file = "activities/solo_yoga.jpg" } }
]
exit_block = { type = "location", text = "Done", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "player", trait = "fitness", op = "add", value = 1 }] } }
```

---

## Type 2: Task

**When to use:** Player is doing a job. Money or trust is the external goal. NPC may be present but work comes first.

**Structure:** Base node → working node with ONE moment of choice → pay + done.

**Examples:** House cleaning ($20), bookkeeping ($25), diner shift ($45), job site ($40), workshop help.

```
NODE: base
  Content: arrive at work
  → "Get to work" → working
  → "Skip today" → exit (nothing)

NODE: working
  Content: the task plays out
  Mid-task, ONE moment happens with a choice:
    → Choice A (costs effort/risk) → higher stat gain
    → Choice B (safe) → lower stat gain
  Exit: money + time passes, done
```

**Design notes:**
- Always two nodes: arrive + work.
- The moment mid-task is WHERE the relationship grows. Not automatic — the player decides.
- The choice should feel natural to the task (not forced romance during bookkeeping).
- Pay is guaranteed regardless of choice. The choice affects NPC stats, not money.
- The moment can vary by relationship stage using a variant chain (group blocks).
- Media: one image at arrival, optionally one during the moment.

**Example:**

```toml
# Base node
[[canvases.nodes]]
id = "base"
name = "The Job Site"
blocks = [
  { type = "paragraph", content = "Workshop. Sawdust and motor oil. Ryan is hauling materials. He puts her to work: holding boards, sorting nails, sweeping." },
  { type = "image", props = { file = "activities/activity_job_site_base.jpg" } }
]
exit_block = { type = "choices", choices = [
  { text = "Get to work", targetType = "node", nodeId = "activity_job_site.working" },
  { text = "Not today", targetType = "trigger", time_progression_minutes = 15 }
] }

# Working node with moment
[[canvases.nodes]]
id = "working"
name = "Side by Side"
blocks = [
  { type = "paragraph", content = "They work and talk. He shows her how to use the table saw — standing behind her, hands over hers on the guide." },
  { type = "paragraph", content = "A heavy board needs moving. He could do it alone, but he looks at her." }
]
exit_block = { type = "choices", choices = [
  { text = "Help him lift it", targetType = "trigger", time_progression_minutes = 180,
    effects = [
      { targetType = "npc", npcId = "npc_ryan", trait = "trust", op = "add", value = 2 },
      { targetType = "player", trait = "fitness", op = "add", value = 1 },
      { targetType = "player", trait = "money", op = "add", value = 40, clamp = false }
    ] },
  { text = "Keep sweeping", targetType = "trigger", time_progression_minutes = 180,
    effects = [
      { targetType = "npc", npcId = "npc_ryan", trait = "trust", op = "add", value = 1 },
      { targetType = "player", trait = "money", op = "add", value = 40, clamp = false }
    ] }
] }
```

---

## Type 3: Hangout

**When to use:** Player chose to spend time with the NPC. No external purpose. The NPC IS the activity. Casual interaction with a menu of options.

**Structure:** Base node is a HUB with multiple choices. Quick choices end immediately (triggers). Deeper choices lead to scene nodes. Higher relationship stats unlock more options on the menu.

```
NODE: base (hub)
  Content: NPC description, setting
  Choices (menu — grows with relationship):
    → "Talk" → trigger (love +1, done)
    → "Play a game" → trigger (trust +1, done)
    → [if love ≥ 8] "Draw together" → node: drawing (scene)
    → [if flirt_unlock] "Sit closer" → node: close (scene)
    → [if kiss_unlock] "Kiss" → node: kissing (escalation)

NODE: drawing (scene from menu)
  Content: the activity plays out
  One choice within:
    → Choice A → stat gain
    → Choice B → different stat gain
  Exit: done

NODE: close (deeper scene from menu)
  Content: physical proximity
  → [if kiss_unlock] "Kiss him" → node: kissing
  → "Stay like this" → done

NODE: kissing → further escalation (chain nodes)
```

**Design notes:**
- The base node IS the menu. This is the only type where the base node has 3+ choices.
- Quick options (talk, play game) are targetType = "trigger" — no extra nodes needed.
- Deeper options lead to nodes that can have their own choices.
- The menu GROWS as the relationship grows. Early game: 2 options. Late game: 5-6 options.
- The player SEES their progress because new options appear on the menu.
- Physical escalation (kiss → handjob → sex) can live as chain nodes within the same canvas, gated by rising stat thresholds. The menu provides the entry point.
- Media: one image at base, optionally one per scene node.

**Example:**

```toml
# Hub node
[[canvases.nodes]]
id = "base"
name = "The Couch"
blocks = [
  { type = "paragraph", content = "Living room. TV on. Ryan takes one end of the couch. The cushion between them is either a buffer or a bridge." },
  { type = "image", props = { file = "activities/activity_tv_couch_base.jpg" } }
]
exit_block = { type = "choices", choices = [
  { text = "Watch the show together", targetType = "trigger", time_progression_minutes = 90,
    effects = [{ targetType = "npc", npcId = "npc_ryan", trait = "love", op = "add", value = 1 }] },
  { text = "Comment on the show", targetType = "trigger", time_progression_minutes = 90,
    effects = [{ targetType = "npc", npcId = "npc_ryan", trait = "love", op = "add", value = 2 }] },
  { text = "Remove the cushion between you", targetType = "node", nodeId = "activity_tv_couch.close",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "npc", npc_id = "npc_ryan", trait_key = "love", operator = "gte", value = 8 }
    ] } },
  { text = "Lean into him", targetType = "node", nodeId = "activity_tv_couch.lean",
    conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" },
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 40 }
    ] } }
] }
```

---

## Type 4: Chain

**When to use:** The activity has depth and branching. Choices at each level lead to different scenes. One path connects forward to escalation or further content. Others are meaningful but shorter. Also used for mini-games, challenges, quizzes.

**Structure:** Multiple levels of nodes. Each node has 2-3 choices that lead to DIFFERENT nodes (not just deeper/exit). One choice at each level is the "forward" path that connects to the next level or escalation. Others lead to shorter scenes or exits.

```
NODE: base
  Content: arrive
  → "Choice A" → node: path_a (leads forward)
  → "Choice B" → node: path_b (meaningful but shorter)
  → "Choice C" → trigger (minimal, done)

NODE: path_a
  Content: scene plays
  Choice:
    → "Continue forward" → node: deeper (gated)
    → "Stop here" → trigger (stats, done)

NODE: path_b
  Content: different scene
  Exit: stats, done (doesn't connect to escalation)

NODE: deeper → further nodes (escalation, challenge results, etc.)
```

**Design notes:**
- This is the most flexible type. The structure adapts to the content.
- Use for activities with narrative depth (drawing sessions, creek swimming, truck rides).
- Use for mini-games (study quiz, cooking challenge, card games).
- Use for physical escalation (the chain of kiss → handjob → oral → sex).
- Each node should have a REAL choice — not just "continue or leave."
- The "right" choice should cost something (attention, money, risk, vulnerability).
- One path connects forward. Others are dead ends but still rewarding.
- Cross-NPC gates can appear on specific choices (e.g., "Tell him about Frank" requires frank_trust ≥ 15).
- Consequence flags can be planted on innocent-seeming choices (pays off weeks later).
- Media: image or video per node as appropriate.

**Example — Relationship escalation:**

```toml
# Entry
[[canvases.nodes]]
id = "base"
name = "Drawing Session"
blocks = [
  { type = "paragraph", content = "Jake's room. Afternoon light. He's set up — sketchbook open, pencils arranged." },
  { type = "image", props = { file = "activities/activity_drawing_jake_base.jpg" } }
]
exit_block = { type = "choices", choices = [
  { text = "Watch him draw", targetType = "node", nodeId = "activity_drawing_jake.watching" },
  { text = "Leave him to it", targetType = "trigger", time_progression_minutes = 30,
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 }] }
] }

# Level 1 — meaningful choice
[[canvases.nodes]]
id = "watching"
name = "Watching Him Draw"
blocks = [
  { type = "paragraph", content = "They talk about art school, his portfolio. His hand moves with a certainty his voice never has." }
]
exit_block = { type = "choices", choices = [
  { text = "Ask about his art school plans", targetType = "trigger", time_progression_minutes = 60,
    effects = [
      { targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 3 },
      { targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 1 }
    ] },
  { text = "Look over his shoulder", targetType = "node", nodeId = "activity_drawing_jake.looking",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "npc", npc_id = "npc_jake", trait_key = "love", operator = "gte", value = 8 }
    ] } },
  { text = "Sketch on your own", targetType = "trigger", time_progression_minutes = 60,
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 }] }
] }

# Level 2 — deeper, gated
[[canvases.nodes]]
id = "looking"
name = "What He's Drawing"
blocks = [
  { type = "paragraph", content = "The drawing is a girl. Your jawline. Your hands. He slams it shut." }
]
exit_block = { type = "choices", choices = [
  { text = "\"It's beautiful, Jake.\"", targetType = "node", nodeId = "activity_drawing_jake.posing",
    effects = [
      { targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 3 }
    ],
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "npc", npc_id = "npc_jake", trait_key = "love", operator = "gte", value = 12 }
    ] } },
  { text = "Pretend you didn't see", targetType = "trigger", time_progression_minutes = 60,
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 2 }] }
] }

# Continues deeper: posing → flirt → kiss → handjob → oral → sex
```

**Example — Mini-game (study quiz):**

```toml
# Question 1
[[canvases.nodes]]
id = "question_1"
name = "First Question"
blocks = [
  { type = "paragraph", content = "Jake flips to a page in his textbook. Taps the diagram." },
  { type = "dialog", content = "What's the derivative of x squared?", props = { speaker = "npc", npcId = "npc_jake" } }
]
exit_block = { type = "choices", choices = [
  { text = "2x", targetType = "node", nodeId = "activity_studying.question_2",
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 2 }] },
  { text = "x squared?", targetType = "node", nodeId = "activity_studying.question_2",
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 }] }
] }

# Question 2
[[canvases.nodes]]
id = "question_2"
name = "Second Question"
blocks = [
  { type = "dialog", content = "Okay, what about sin(x)?", props = { speaker = "npc", npcId = "npc_jake" } }
]
exit_block = { type = "choices", choices = [
  { text = "cos(x)", targetType = "trigger", time_progression_minutes = 90,
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 2 }] },
  { text = "I have no idea", targetType = "trigger", time_progression_minutes = 90,
    effects = [{ targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 }] }
] }
```

---

## Type 5: Scene (Experimental)

**When to use:** Hybrid of Hangout and Task. Player is WITH the NPC doing something together. The activity flows as a narrative with 1-2 embedded choices. Not a menu, not a job — a shared experience.

**Structure:** Base node → scene node with 1-2 natural choices → optional gated exit to chain nodes for escalation.

```
NODE: base
  Content: arrive, NPC description
  → "Join them" → scene
  → "Leave" → exit (minimal)

NODE: scene
  Content: the activity plays out as narrative
  One choice embedded naturally:
    → Choice A (engaged, costs something) → higher stats
    → Choice B (passive, safe) → lower stats

  Then exit options:
    → "Done" → trigger (time passes, done)
    → [gated] "Something more" → node: escalation (Chain takes over)
```

**Design notes:**
- This type is experimental. Use it when Hangout feels too flat and Chain feels too complex.
- The scene should flow like prose — the choice emerges from the narrative, not from a menu.
- The gated exit at the end bridges Scene into Chain for physical escalation.
- Only 1-2 choices per scene node. Keep it simple.
- Good for: cooking together, morning coffee, afternoon walks, shared quiet moments.

**Example:**

```toml
[[canvases.nodes]]
id = "base"
name = "The Kitchen"
blocks = [
  { type = "paragraph", content = "Kitchen. Frank is chopping vegetables. Sleeves rolled. He nods at the cutting board." },
  { type = "image", props = { file = "activities/activity_cooking_frank_base.jpg" } }
]
exit_block = { type = "choices", choices = [
  { text = "Pick up the knife", targetType = "node", nodeId = "activity_cooking_frank.cooking" },
  { text = "Set the table instead", targetType = "trigger", time_progression_minutes = 90,
    effects = [{ targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 }] }
] }

[[canvases.nodes]]
id = "cooking"
name = "Side by Side"
blocks = [
  { type = "paragraph", content = "Side by side at the counter. He talks about Diana's old recipes. His voice softens when he mentions her mom." }
]
exit_block = { type = "choices", choices = [
  { text = "Ask about Diana", targetType = "trigger", time_progression_minutes = 90,
    effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "love", op = "add", value = 3 }
    ] },
  { text = "Focus on the food", targetType = "trigger", time_progression_minutes = 90,
    effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 2 }
    ] },
  { text = "Reach past him for the skillet", targetType = "node", nodeId = "activity_cooking_frank.close",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "love", operator = "gte", value = 12 }
    ] } }
] }
```

---

## Choosing the Right Type

| Question | Answer → Type |
|----------|--------------|
| Is the player alone? | Yes → **Solo** |
| Is the player doing a job for money? | Yes → **Task** |
| Is the activity casual with multiple small options? | Yes → **Hangout** |
| Does the activity have narrative depth with branching? | Yes → **Chain** |
| Is it a shared moment that flows naturally? | Yes → **Scene** |

**Multiple types can exist in the same game.** A typical game might have:
- 3-5 Solo activities (yoga, jogging, shower, nap, journal)
- 2-4 Task activities (cleaning, bookkeeping, diner shift, job site)
- 2-3 Hangout activities (TV couch, park bench, general hanging out)
- 3-5 Chain activities (drawing sessions, truck rides, creek swimming)
- 2-3 Scene activities (cooking dinner, workshop help, morning coffee)

**The type is decided per activity, not per game.** Different activities suit different formats.

---

## Substance Checklist

Regardless of type, every activity with an NPC should include at least one of:

- [ ] **Choice that costs something** — money, risk, vulnerability, or effort for better stats
- [ ] **Stats from right choice** — the engaged option gives more than the passive option
- [ ] **Variant content by relationship stage** — the scene feels different at love 5 vs love 25
- [ ] **Gated escalation** — higher stats unlock deeper interactions (especially in Chain/Scene)

Optional but valuable:
- [ ] **Cross-NPC gate** — a choice requires investment in another NPC
- [ ] **Money choice** — spend money for bonus relationship stats
- [ ] **Consequence flag** — an innocent choice sets a flag that pays off later
- [ ] **Item gate** — requires a specific item/flag to access an option

---

<!--
## Future: Group Type (not yet implemented)

**When to use:** Multiple NPCs present. Player navigates group dynamics, chooses who to focus on.

**Structure:** Base node describes the group setting. Choices determine which NPC gets attention/stats. Tension between NPCs visible in the scene.

**Examples:** Breakfast, dinner, hiking, power outage, group trip.

```
NODE: base
  Content: group setting, all NPCs described
  → "Talk to Jake" → node: jake_focus (jake gets stats)
  → "Sit by Ryan" → node: ryan_focus (ryan gets stats)
  → "Help Frank" → node: frank_focus (frank gets stats)
  → "Stay neutral" → trigger (everyone +1, done)
```

Dropped for now. Revisit when implementing meal canvases and multi-NPC scenes.
-->
