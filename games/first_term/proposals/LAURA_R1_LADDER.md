# [READY] Laura, release 1 — the good mom, lonely

> Signed by LO: LO, 2026-11-01 ("Go ahead"). Cut to four steps 2026-11-01 (LO: "Yes do the fix"). Step 5 of the release-1 redesign (DECISIONS 99–105), person 1 of 6.
> Designed against `sheets/TASTE_COLUMNS.md`; scope from `sheets/RELEASE1_SCOPE.md` (both signed 2026-11-01).
> Built steps and places: `sheets/people/npc_laura.md` and `toml_phases/5_scenes.toml`. On LO's sign this
> becomes her person sheet's ladder and one scene sheet per changed step. Media: a declared block counts as
> present; the harvest stays LO's.

## The frame
Laura is 41, Ella's mom, married to Mark, who hasn't looked at her like that since the wedding. She wants a
happy house and her good girl close. She is lonely, and she hides it. **No sex between them, no kiss.** The
heat in her ladder is what Ella sees: her mother alone, wanting. Laura is also the house's witness: she
opens Ryan's door, waits up on the stairs, watches Jake at the front door.

## Already built, and it carries her ladder
- **`laura_alone_in_bed`** (Sun–Fri 22:00–23:00, Mark downstairs): through the gap in her door, Ella sees her
  mother finger herself. "Keep watching" pays Corruption +1, cap 19 (DECISIONS 82). Once a night.
- **`master_door_saturday_night`** (Sun 00:00–01:00): through the gap, Mark takes Laura. Staying pays
  Corruption +1, cap 19 (DECISIONS 79–80). Once a week.
- **New, the shower** (LO, 2026-11-01: "Both"): Saturday 16:30–17:00, before she dresses, Laura showers. The
  bathroom lock sticks halfway, as it always does (`2_one_shots.toml`, the opening), and the door doesn't
  close. Through the steam on the glass Ella sees her mother's hand between her legs under the water.
  "Keep watching" pays Corruption +1, cap 19, the same as the bedroom gap. Once a week. It needs a new
  schedule row: `home_bathroom`, Sat 16:30–17:00.
- These are the hot repeatables this ladder pays off. The new top step is the night Laura sees her there.

## The numbers (rule 5: her meter is the lock)
- **Her lock is Love (Warmth).** Want, her desire meter, is **no longer read by her steps**: a good mom.
- **Four steps, one per first** (LO, 2026-11-01: sized by firsts, not by a count; `ARC_CRAFT_STUDY.md` §1: side
  people 4–6 steps, and a step that only waits is a bridge).
- Each step pays **Love +5**; each needs **10 more** than the last (none, 10, 20, 30).
- **Her plain items pay Love +2, once a day in total** (breakfast, coffee, dinner, cooking, dishes, wine, a film,
  studying at the table, her hair). Today each pays +1 to +3 on its own daily brake (`laura.py` has 20 `warm(L)`
  raises), so several a day fill her Love on their own. One a day makes it **two or three days between steps.**
- Her suspicion (`laura_suspicion`) and its costs stay as built: lies, the curfew, "she'll know".
- **Her rule stays:** in a room Laura is in, the house's hot buttons don't show, or she catches it (Love −3).

## The ladder

| # | step | where · when | gate | status |
|---|---|---|---|---|
| 1 | Blue dress | her room, Tue 18:00–22:00 | none | built (`laura_01`); pays Love +5 and Exhibitionism +3 (not Want +10) |
| 2 | Wine in the kitchen | kitchen, Mon/Tue/Thu/Fri 20:00–22:00 | Love 10 | built (`laura_03`); gate Love only |
| 3 | **All dressed up** | her room, Sat 17:00–18:30 | Love 20 | built as `laura_06` "take me with you"; **reworked** |
| 4 | **She saw you** | her door, Sun–Fri 22:00–23:00 | Corruption 20 · Love 30 · step 3 done · Ella watched through a gap (bedroom or shower) 3 times | **new, top step** |
| — | *Laura C 7 (the stairs kiss), Laura C 8 ("it wasn't the wine")* | | | **cut** |

**Moved to their owners, not cut.** These stay in the game with Laura in them, but they stop being her steps
and stop setting `laura_step`:
- **Home late** (`laura_02`), her waiting on the dark stairs: becomes the **curfew rule**, a repeatable that
  fires whenever `came_home_late` is set (it already reads it), owned by her suspicion, not her ladder.
- **Ryan's door** (`laura_04`), her opening his door on Ella's feet in his lap: becomes **an event on Ryan's
  ladder** after his step 4, the next evening on the couch repeatable. Ryan's sheet is re-signed for it.
- **Jake at the door** (`laura_05` = Jake 4, one canvas): becomes **Jake's step only**, with Laura watching
  from the dark. Jake's sheet carries it.

## Each step, by the seven columns

| # | the moment | who sees or knows | what she risks | how Ella says yes | Laura's move | does it finish | what changes after |
|---|---|---|---|---|---|---|---|
| 1 | Laura gives her the blue dress she can't wear any more: "It never fit me like that." | Laura | — | she tries it on | the gift, and her hand on the hip | yes | the dress is Ella's; Laura's line on it |
| 2 | two glasses poured; "Mark hasn't looked at me like that since the wedding." | Laura's secret is Ella's | — | she sits and drinks with her | the second glass, poured before Ella came down | yes | Ella knows she's lonely |
| 3 | Ella zips her mother into her good dress. Mark calls from downstairs that he's going to the bar. Laura sits on the bed, dressed up, with nowhere to go. | Ella; Mark, not looking | — | "You look beautiful, Mom." · or she says nothing | she asks to be zipped, then asks, "Do I still look like someone you'd look at?" | yes | `laura_lonely`: the alone-in-bed line now names this night |
| 4 | Through the gap: Laura comes, biting the back of her hand, and when her eyes open they're on the door, on Ella | **Laura sees Ella** | being caught watching her mother | she stays at the gap (Curious) | after: she doesn't pull the sheet up fast. She says, quietly, "Go to bed, sweetheart." | **yes**: Laura finishes before she sees her | breakfast: "We don't talk about last night." · her door: below |

Her voice (rule 7): a low line (Ella under the stage: "That's your mom. Go to bed.") and a high line (over it:
"She's lonely, and you can't stop watching her be lonely.") on each step's sheet.

## Step 4, "She saw you", more closely
- **When:** a weeknight 22:00–23:00, the `laura_alone_in_bed` gap, after Ella has kept watching three times
  (a counter on the existing button) and after step 3.
- **The act** is Laura's, alone, and shown to its end (rule 5): her hand under the sheet, her breath, her
  thighs, biting the back of her other hand so Mark won't hear. Laura's crude words are her late column,
  "pussy, wet" (`spine/SP2_ladders.md:192`). LO confirms on the scene sheet.
- **Then** her eyes open on the door. Ella's choices: **"Step back from the gap."** · **"Stay where she can
  see you."** (Curious) · either way Laura says "Go to bed, sweetheart."
- **After it:**
  - breakfast, next morning: "We don't talk about last night." Ella's answer: "Okay, Mom." (Love +5) · "You
    should talk to Mark." (suspicion −5, Love +2).
  - **the gap after step 4:** the repeat still runs. Now Laura knows, and her line changes: she turns her face
    to the wall, quieter. Whether the gap gets wider is a later release.
- **What she whispers** as she comes: **"Ryan."** Not Mark's name (LO, 2026-11-01). Ella hears it.
  - It's a hook for a later release: Laura wants her step-son. In release 1 it is only the name, and Ella's
    thought beside it. Nothing else of Laura's reads it.
  - It ties into Ryan's ladder, where Laura already watches: she opens his door at his step 4, and her light
    is on across the hall at his step 8 (and the moved "Ryan's door" event). A flag `laura_said_ryan` is set, for later.
- **The counter** for step 4 counts both gaps: the bedroom and the shower.

## The ladder rules, ticked

| rule | result |
|---|---|
| 1 every step adds a witness, risk or yes | pass: 2 her secret, 3 Mark not looking, 4 Laura seeing Ella |
| 2 the top step is a payoff | pass: step 4 pays off the gaps Ella kept returning to, a known person, finished |
| 3 one cut-off | pass: none |
| 4 she moves every other step | pass: Laura acts in every step (the gift, the second glass, the ask, her own act) |
| 5 her meter is the lock | pass: Love +5 a step against +10; one item a day at +2 |
| 6 one hot repeatable per stage | **declared exception:** Laura isn't a heat ladder before step 4. Her hot repeatables are the two built gaps and the new shower gap, open from Good Girl |
| 7 her voice changes with her level | pass |
| 8 something happens after the top | pass: the breakfast, the changed gap |

## Cut, and what the player loses
- **Laura C 7**, the kiss on the dark stairs at Zoe's party, and **Laura C 8**, "It wasn't the wine." / "I'm your
  mother." Laura's climb toward Ella is gone. Built step 6's old promise, "Take me with you one night", goes with it.
- **The 17 placeholder tease and touch screens** on her plain items (`laura.py:377`, `:380`). They were never
  written; mother-daughter teases are against "good mom". The plain items stay.
- **Want as her lock.** The Want meter stays in the game but nothing of hers reads it.

## Decided with LO (2026-11-01)
- The name she whispers at step 4: "Ryan."
- The room and the shower: both, this release.
