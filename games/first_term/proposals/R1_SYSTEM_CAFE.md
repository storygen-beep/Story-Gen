# [READY] Release 1 system 3 — the café customers

> Signed by LO: LO, 2026-11-01 ("Signed next"). Step 4 of the release-1 redesign (DECISIONS 99–103), system 3 of 4.
> Model: `scout/cafe_customers.md` (IHOH's diner, with corrupted-city's and CoT's River Rat as contrasts).
> Changes the signed `sheets/systems/job.md` and `sheets/people/npc_gary.md`; on LO's sign they are rewritten
> to match and re-signed. Pay and tips fit `proposals/R1_SYSTEM_RENT.md` ($8 a shift plus tips).

## LO's direction (2026-10-31)
"Tom stays strict boss, no selling her to customers. Instead initially customers are doing those things, and
once she is corrupted things can move forward. Tom might realise this and say that this is not good as café
reputation is hurting but fine as customers' footfall has increased. We can find some ways for her to corrupt
Tom too." Release-1 scope: Tom's uniform push and booth four are cut; his lust is a later release.

## What the top games do (from the scout card)
- **IHOH:** the boss never sells her. Customers go look, comment, grab; **she chooses each time**; going along
  **doubles the tips**; one regular becomes a named man. But it keeps no reputation counter, and the scenes
  don't grow with her stats.
- **corrupted-city:** the diner gets busy, and her name follows her into the street: "The diner is always
  packed now." (The boss sells her there; we don't take that part.)
- **CoT River Rat:** the owner holds a line ("that's not appropriate"), and changes the uniform only after her
  flirting has already changed the room.

## The design

### 1. A shift
Clock in · **one customer scene, drawn from the pool for her level** · clock out with **$8 plus that
shift's tips**. One shift on weekdays, two on Saturday (rent sheet). The scene is never the same two shifts
running: each level has a pool of 4–6, drawn without repeats until it runs low (IHOH's shuffled deck).

### 2. Three levels: the customers go further as she does

| level | opens at | what the customers do | her choices | tips |
|---|---|---|---|---|
| **1 · They look** | the job | eyes on her when she bends to a table; a table whispering when she walks away | none needed: the scene is the room watching | $2–4 |
| **2 · They say it** | Daring (Exhibitionism 20), or the sexy uniform on | "Are you on the menu?" · a guy asks what time she gets off · a table rates her out loud | **play along** (showing yes: leans over the check, Exhibitionism +1) · **flirt back** (doing yes: Corruption +1) · **"Not tonight, hon."** | $4–8; playing along $6–10 |
| **3 · They touch** | Curious (Corruption 20) **and** Daring (Exhibitionism 20), after three level-2 shifts | a hand on her ass when she leans over · a hand up the back of her skirt at the counter · a guy pulls her onto his knee to "say thanks" | **let it** (both meters +1: it's seen and it's touch) · **pull away**, polite ("Your food's here, sir.") · **slap it away** (he leaves, no tip) | $4–8; **let it: doubled, $10–16** |

- **The sexy uniform is her choice** (Tom doesn't push it). It opens level 2 early and adds +50% to tips.
- **The no is written at every level** and costs only tips. Never her job (Tom stays strict).
- Levels 4 and up (under the table, the back room, the regulars as a group) are a later release, with the
  locked button naming the number.

### 3. One regular becomes a named man: Gary
- Gary (52, booth four, already in the game) is the face that comes back, like IHOH's Mr. Jones.
- He shows at each level: level 1 he lowers his paper; level 2 he says it; level 3 his is the hand she lets
  stay, or not. He tips more than strangers (+$4) and remembers what she let him do last time.
- His own route (asking her out, more) is a later release. Booth four's "ten minutes, $20, Tom takes half"
  stays cut: Tom never sells her.

### 4. The café keeps score
- **Two counters on the café:**
  - **footfall** goes up +1 every shift she plays along or lets them;
  - **name** goes down −1 every shift she lets them touch.
- At **footfall 10**, the tables are fuller: the shift scenes show more men waiting, and tips +$2.
- At **footfall 15 and name −5**: **Tom's top step** this release. He watches a customer's hand on her, and
  her letting it, then takes her into the back: "Reputation's going. The tables are full." He doesn't stop it,
  and he doesn't sell it. He draws one line, CoT style: "Not by the window." (Taste: who sees, Tom; his move,
  the line; what changes after, the window rule and Tom's look.) This is where her corrupting Tom starts, in a
  later release.

### 5. The café reaches the rest of her life
- **The street** (system 2's once-a-day witness): from footfall 10, a man in the street knows her: "You're the
  girl from the café." (corrupted-city's fan, without the price.)
- **Home:** at Mark's Sunday table, from footfall 10: "Good tips this week. What are they tipping for?" Ryan,
  if his Lust is 40+: "Some guys from the yard said they went to your café."

## Against the taste columns
| column | here |
|---|---|
| who sees | the room, every shift; Gary, who comes back; Tom, at the top |
| what she risks | being seen letting it; the café's name; Tom's line |
| how she says yes | two kinds at levels 2 and 3 (a showing yes and a doing yes), plus the no |
| his move | the customer's: the comment, the hand. Hers to allow |
| does it finish | yes: each scene ends with the tip, and the line about what she did for it |
| what changes after | footfall and name; the fuller room; Tom's window rule; the street and the house know |

## Engine and build work (for after the sign)
- Shift pay `money(8)` plus a tip effect per scene (`cafe.py`); the tip range by choice.
- Per-level pools drawn at random: the home random events already draw (1 in 4); **check before building**
  whether a canvas can pick one of N scenes without repeating until most are seen, or whether a cycling POOL
  of nodes does it.
- Two traits on the player for the café: `cafe_footfall`, `cafe_name` (signed range −20…+30).
- Tom's top step: one canvas at the café, gated by both counters.
- The street line and the two home lines read `cafe_footfall`.
- Gary's sheet rewritten: met at level 1, not at booth four.

## Not decided here
- Ladies' night and the team in the side room (IHOH's two side kinds): later releases.
