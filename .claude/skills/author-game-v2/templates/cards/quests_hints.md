# Card — Quests and hints (infrastructure: a view)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/quests_hints.md` and `round9b/traces/quests_hints.md`. Models: **Course of
> Temptation (CoT)** hint cards, **In Her Own Hands (IHOH)** hint journal, **Shady Deals (SD)** whiteboard
> and Red Phone.
>
> **Infrastructure, not a system** (`the-systems.md` SY1): declare it in `board.infrastructure[]` as
> `{ "name": "quests_hints", "kind": "view" }`, never in `board.systems[]`. It carries or shows other
> systems; it has no ladder of its own. It is a required view on every arc, not a system.

| field | the models | cite |
|---|---|---|
| what it is | CoT: a sidebar Hints button that glows until first opened; IHOH: a side-menu journal; SD: a whiteboard at home plus a Red Phone in Contacts | [StoryCaption]; [Progress_Hints_Base]; [Whiteboard]; [Contacts] |
| what it shows | CoT 25 cards, 106 steps; IHOH 9 paths, 127 done markers, 149 tip tiles; SD 7 numbered goals | round 9b `cards/quests_hints.md` |
| how a step shows | CoT shows only the latest true step, "Keep exploring!" if none, a completed card when all are true; IHOH shows every step as a tile: done, next in her voice, or locked | [StoryHintWidgets]; [ShaunPathHints] |
| rules: cost | none, it is a menu; SD's whiteboard is a walk home, the Red Phone a call | round 9b `cards/quests_hints.md` |
| memory | none of its own: each step reads the arc's flags; IHOH done tiles double as a diary | `cot_37_database_storyhints.js:43-57`; [ShaunPathHints] |
| closed state | IHOH greys a path her choices closed ("No further progress possible"); CoT has an "end" step on only 2 of 25 cards | [Progress_Hints_Base]; round 9b `traces/quests_hints.md` |
| a live query | SD's Red Phone: 12 questions, 3 answer from her live state ("Who or what haven't I found out about yet?") | [Red Phone] |
| the gate at the choice | CoT: 46 `hintskillgate` calls print "There are hidden options here. Maybe if your Exhibitionism were higher…" | round 9b `traces/quests_hints.md` |
| the systems it serves | CoT: 15 of 24 systems (63%) and 12 of 22 recurring NPC roles (55%) have a card; IHOH: one path per person plus Work and My Life | round 9b `cards/quests_hints.md` |
| sizes | CoT 3–7 steps a card; IHOH 5–54 tips a path | round 9b `cards/quests_hints.md` |
| what a step names | CoT: a place 18%, a time 10%, a stat 3%; IHOH: a place 26%, a time 30%, a stat 2% | round 9b `cards/quests_hints.md` |
| exception | SD's whiteboard gates the crew: all 7 goals true opens "Organize your own crew." | [Whiteboard]; [Band Creation] |

## Measured floors (directions, never gates)
- One card per arc and per lewd ladder; CoT misses 37% of its systems (round 9b `cards/quests_hints.md`).
- 3–7 steps a card (CoT).
- Each step names place, time and the gate; CoT does so in 18% / 10% / 3% of steps.
- One "what haven't I found" query from live state (SD Red Phone, 3 of 12 questions).
- A visible closed state: 8 of IHOH's 9 paths can close, and a closed path turns grey.

## What players say
- I know the step but it doesn't fire: 23 of 64 hand-read how-tos, e.g. *"I'm stuck on the tip that says take
  advantage when he comes from the club but when I go to meet him in the kitchen nothing happens?"* (IHOH,
  mopoga#137498). Name the gate in the step.
- What's next: 24 of 64, even on an arc with a card, e.g. *"How do you progress in the Harasser storyline"*
  (CoT, mopoga#75597).

## Our engine today (round 9b §6)
- SUPPORTED: `TemplateQuest` (`template_import.py:930`) and a `quest` condition (`v2.py:5094`).
