# craft/walk-ins.md — what she walks into, who walks in on her, and who comes to her

Read this before you write a card for a scene that waits at a place: something she walks into (a couple behind the boathouse, a fight on the stairs), someone who walks in on her in the middle of an act (a housemate at the bathroom door), or someone who comes to her when she arrives (the neighbour waves her over at the gate). The plan's walk-ins bite (`plan.md` §8) lists them, area by area; each area's scenes are one piece.

**Three kinds, our design** (LO, typed in main-lean 2026-11-26: "Yes", "One is fine for now"; the measures are the study's, `COT_DESIGN_STUDY.md` Part 9 and `playtest_study_20261109/13_random_scenes_top.md`):
- **(a) She comes across something:** it fires by itself when she arrives, behind a chance: the couple under the bridge, her housemate's door open a crack. Her choice inside is to look or leave. It is off the shared one-a-day flag; each one is once a day on its own. Its card's Does: names `she comes across something` on its first screen.
- **(b) Someone comes to her:** it fires by itself when she arrives, hand-written for one named person, only where that person's rows put them ("When someone comes to her", below). The world's choice to reach her. These share the one-a-day flag. When its words need her in the middle of something (lifting, eating, studying), it fires inside that act instead, never on arrival (C2196).
- **(c) She gets noticed:** it fires by itself when she arrives, behind a chance, and only in the clothes it is about: the guys at the bus stop go quiet at her leggings. Strangers are allowed; no named person is needed. It is off the shared one-a-day flag, once a day on its own, and its card's Does: names `she gets noticed` ("When she gets noticed", below; C2200; LO, typed in main-lean 2026-11-27: "Yes, we should align our place description to it. And for scenes like leggings ones, those should be walkins right??", "dont we need skill changes").

All three fire on arrival and none is a button (C2195). Why: the study's players say surprises are too rare (CoT's walk-ins fire on arrival, `COT_DESIGN_STUDY.md` Part 9), and a button she must find and press is no surprise. LO chose it, typed in main-lean 2026-11-26: "2nd one" (of: keep the buttons and mark them, fire on their own, a mix), then "Go" to the picks below. That reverses his "2 i would say button is good here" for walk-ins.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C788 | random scenes are people: about 45 words, half everyday, nearly half with a choice; who is there and what they want sets the tone | L147 | a walk-in | reader |
| C802 | the world is more than her body: about half of the events are everyday life (65% early): other people's lives, small social moments | L147 | the plan | reader |
| C678 | at least half of these scenes name a person she knows | — | the plan | note |
| C854 | count the pool once, and credit each scene to the system it belongs to | — (the count) | the plan | note |
| C855 | each scene is filtered by hours, who is here, what she wears, her meters, days since | — | a walk-in | note |
| C856 | about half carry a time window | — | a walk-in | note |
| C857 | the pool opens as she changes: at least 3 of her states open new scenes | — (later releases) | the plan | note |
| C858 | a place she visits several times a day needs many scenes, each spaced a day or more apart | — (later releases) | the plan | note |
| C859 | pure chance annoys; a scene can also take something, not only add | — | a walk-in | note |
| C28 | the taboo-at-home shape runs on walk-in risk: each housemate has at least one walk-in at home | — (the person pass) | the plan | note |
| C1820 | the odds ride the same meter as the content: chance bands 0.10 / 0.35 / 0.70 into one canvas banded watch / touch / act | — (how it grows) | a walk-in | note |
| C724 | walk-in odds read her climb; flat odds are listed | — | a walk-in | note |
| C1821 | three parts: the router (substitutions on the act), the branch (one `substitution_only` canvas with bands), the payoff (into a rung that exists) | — | a walk-in | note |
| C1864 | band with a rule's `conditions`; in an exclusive group, append a new rule last | — | a walk-in | note |
| C792 | a walk-in is two screens: the moment, and one answer screen per choice; a third screen is the defect | — | a walk-in | note |
| C302 | peek or catch: an option is added each stage, and being caught becomes a door | — | a walk-in | note |
| C1262 | see `craft/body-moments.md` |  |  |  |
| C212 | see `craft/arc.md` |  |  |  |
| C174 | see `craft/arc.md` |  |  |  |
| L97 | a walk-in only fires where the walker's rows put them, and it shows what they were already doing | first_term's walk-ins almost never fired; a TV walk-in swapped her film for its own | a walk-in | reader |
| L70 | see `craft/meters.md` |  |  |  |
| L147 | the world felt empty: 69 of first_term's 82 random scenes were about her body | the lesson itself: 69 of first_term's 82 random scenes were about her body (`lists/LESSONS.md`) | the plan | reader |
| L150 | no "nothing happens" scene, anywhere | first_term had them; LO cut them all | a walk-in | reader |
| L4 | plan from the study's answer and its target, not from the tools already built | first_term planned 10 random events because a helper existed, and reached 19% of ~50% | the plan | reader |
| C2186 | someone comes to her: a scene that fires by itself on arrival, written for one named person, only where their rows put them: at her place (`requires_npc`), or next door, coming to her (an `npc_at_location` on the adjoining place); about half are everyday | first_term_lean has none: every scene at a place is a button she must find, and the study's players say surprises are too rare (Part 9) | a walk-in | script + walkins |
| C2187 | at most one "comes to her" scene a day across the whole game: one brake flag every such scene waits on and sets on every way out, cleared in `[engine.daily_tick]`; kind (a) and story moments are outside the limit | — · kept blocking: LO's "One is fine for now" | a walk-in | script + walkins |
| C2188 | always a written way out, with its own line; a no is free while her meters are frozen, and costs a little with that person once feelings move | — · kept blocking: LO's "Yes" (2026-11-26); every study game has one (Part 9) | a walk-in, a no is possible | reader + walkins |
| C2189 | a repeat rests or climbs one step (each step needs the one before); it never replays at once. The rest before the same scene comes again is set per game, LO's call, on the plan (worked example: three days) | — (LO's "Yes"; the rest, LO, typed in main-lean 2026-11-26: "Go with your picks") | a repeatable | note |
| C2190 | a story moment fires for sure when it is due, never behind a chance | — · kept blocking: LO's "Yes" (2026-11-26); same lesson as C174 | a person's arc step | script + walkins |
| C2191 | bolder answers open by her level, once her meters move | — (later releases; LO's "Yes") | a release after the first | note |
| C2192 | release 1: 8 to 10 "comes to her" scenes, and the first steps of two or three chains, flags only | — (the count; LO's "Yes") | the plan | note |
| C2195 | a walk-in she comes across fires by itself on arrival, never a button: `trigger_mode = "random"` at its place, `chance = 0.35` by default, `max_triggers_per_day = 1`, gated by the person's presence and hours as before; it stays off the shared "comes to her" flag, and the place rests 3 arrivals after a hit (the engine's `random_cooldown`); her choice inside is unchanged | the study's players: surprises too rare (Part 9) · kept blocking: LO, typed in main-lean 2026-11-26: "2nd one", "Go" | a walk-in | script + walkins |
| C2196 | a scene that comes to her fits what she is doing and wearing when it fires: on arrival she has only just walked in; when its words need her in the middle of an act (lifting, eating, studying, washing), it rides on that act as a substitution rule, after the act's costs, never on arrival | first_term_lean's `marco_hips` (P49) fired on walking into the gym, with no workout, no day pass and no gym clothes, and its words fixed her squat: "Your stance is all wrong", his hands turning her hips. LO, typed in main-lean 2026-11-26: "This ones a walkin right, she didn't have gym membership yet. And she is working out in this scene. Why??", then "Go ahead." | a walk-in | reader + walkins |
| C2200 | she gets noticed: a stranger reacts to what she is wearing, as a scene that fires by itself on arrival (`trigger_mode = "random"`, `chance = 0.35`, `max_triggers_per_day = 1`), gated by a clothing condition and the hours people are about; off the shared flag; two screens and a written way out; at most a quarter of the game's arrival scenes. Never a line in the place description (`craft/places.md` C2201) | first_term_lean: the street, park and gym descriptions noticed her leggings and Mom's things, the same words on every visit, with no choice (LO, 2026-11-27) | a walk-in | script + walkins |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **A scene she comes across** is a canvas whose `trigger.location` is the place, with `trigger_mode = "random"` and `chance = 0.35` (a game may pick its own, on the plan with LO's words), and `max_triggers_per_day = 1`, which makes it once a day (read at v2.py:15120, checked at v2.py:6913-6922). The person's presence and hours gate it as before: their rows, `npc_at_location` or `requires_npc` (v2.py:6948-6961). After a hit the place rests 3 arrivals, the engine's default `random_cooldown` (v2.py:6979-6981).
- **A scene behind a chance is never a button.** `trigger_mode = "random"` and `chance` on its trigger (read at v2.py:15252-15259) make it fire by itself on arrival: the place's passage calls `setup.getStoryCanvasRedirect` (v2.py:11490, 6555), which runs `setup.checkRandomEncounters` (v2.py:6866-6986). That rolls each eligible one and sends her into the first hit. Every button path skips a random canvas (v2.py:4625, 4736, 5946, 5977, 6009, 6603, 6726). The roller that once showed a button by chance, `setup.selectCanvasByPriority` (v2.py:6488), is called from nowhere. So every walk-in at a place, kind (a) or kind (b), is a random canvas; what keeps them apart is the label on the card and the shared flag (kind b only).
- **Someone walks in on her** is a rule on the act she is doing: `[[canvases.trigger.substitutions]]` with `target_canvas_id`, `chance` and conditions (v2.py:14801-14811). `setup.checkAndSubstituteCanvas` (v2.py:7009) runs it when she starts the act; each rule rolls its own dice and the first that hits wins (v2.py:7047-7054). Rules that share an `exclusive_group` (read at v2.py:14738) share one roll instead, and groups go before the independent rules (v2.py:7003-7008, 6967-6991). An `npc_at_location` condition reads the person's rows: `scripts/who_is_where.py` shows where the rows put them.

## The shape

1. **After the schedules.** A walk-in sits where a person's rows already put them, so the schedules come first (L97).
2. **Per area, per place:** one or two scenes. For each, say which kind it is: she walks in on something, or someone walks in on her.
3. **Who.** Half or more name a person she knows (C678). Strangers fill the rest.
4. **Everyday, about half.** A person doing their own thing, a small social moment, their life going on without her (C802, C788). The other half may be about her body or what she sees. Count the share across the area before the card, and write the count on the card (L4).
5. **Her choice.** Each scene asks her something. She watches or she leaves; she helps or she says she's late. Every button has its own line after the click, and leaving is written, not a silent exit.
6. **The window.** From the person's rows, not a guess. Someone walking in on her comes from their neighbouring row and is still doing it: the towel over his shoulder, the mug in his hand (L97). Never a second version of what they do.
7. **How often.** It fires on arrival at `chance = 0.35`, once a day (`max_triggers_per_day = 1`), or once ever (`is_repeatable = false`). Say which on the card (C2195).
8. **What it pays.** While her meters are still (release 1), a scene sets a flag only and pays nothing. When meters move, a meter's first gain is never behind a chance roll (L70); a chance scene can repeat a gain, never be the first.
9. **Never empty.** No scene of "nothing happens" (L150). If a place has nothing, it gets no scene.
10. **The arc first.** If a person's next step is ready, it is its own scene with no chance on it, and the walk-ins with that person wait behind it (C174, C212).
11. **Seeing is not her sex.** Sex she sees or hears is a walk-in. Her own sex opens only with a partner (`plan.md` §10).
12. **The person pass.** Beside the place pass, take each person she lives with or sees often and ask: when this person is alone, what are they doing right now, at this point in their arc? Their rows give the where and the when. In a taboo-at-home game, each housemate has at least one walk-in at home (C28).
13. **The person now, not their end want.** A walk-in shows where the person is in their arc today. A person who wants her later does not want her in their first walk-in. A new version comes only when their arc moves a step, and each version is still what they were already doing (L97). (LO, relayed 2026-11-21: "in the starting ryan doesnt want her.")

## Worked example

Roles, not a world: a riverside park in her area, a neighbour she knows, two strangers, and a lodger at home. Word counts are for the story text.

**A · Everyday, a person she knows** (40 words). Fires on arrival at the park, 07:00–10:00, while the neighbour's row puts him on the path: `trigger_mode = "random"`, `chance = 0.35`, once a day. Does: `<canvas>.<node> | a walk-in, she comes across something, …`.
> The neighbour is on the bench by the gate, his dog's lead wrapped twice round his fist.
> "You. Hold him a minute? My laces." The dog is already pulling toward you.
> You blink. He's never asked you for anything before.

| button | the first line after the click |
|---|---|
| "Take the lead" | *The dog drags you two steps. He laughs, the first time you've heard it.* · sets `held_the_dog` |
| "Sorry, I'm late" | *"Course you are." He bends to his laces without looking up again.* |

**B · She comes across something, strangers** (53 words). Fires on arrival on the path under the bridge, 19:00–21:30, `chance = 0.35`, once a day.
> Under the bridge it's darker than the path. Then you hear it: a gasp, a belt buckle, skin on stone. A woman is pinned to the wall with her skirt up round her waist, and the man's hips slam into her, slow and hard.
> Your face is burning, and your feet don't move.

| button | the first line after the click |
|---|---|
| "Watch" | *She sees you over his shoulder. She doesn't stop. Neither do you.* · sets `saw_bridge_couple` |
| "Back up the path" | *You're back in the light with your heart going like you ran.* |

**C · Someone walks in on her** (42 words). A rule on her act "Do your laundry" in the utility room: the lodger, from his evening row in the kitchen, when he is there by his rows. Chance 0.25.

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "laundry_lodger_walks_in"
chance = 0.25

[canvases.trigger.substitutions.conditions]
version = "1.0"
logic = "AND"

[[canvases.trigger.substitutions.conditions.items]]
type = "npc_at_location"
location_id = "kitchen"
npc_id = "npc_lodger"
operator = "is_present"
```

> You're bent over the machine, dragging out wet sheets, when the door opens. The lodger, his dinner plate still in his hand. His eyes go straight to your ass in your sleep shorts.
> "Sorry. Wanted the bin." He doesn't move toward it.

Buttons: "Straighten up" · "Keep pulling the sheets out". Each opens on one line of his reaction. In release 1 it sets `lodger_saw_laundry` and pays nothing.

The area's count, on the card: A is everyday, B and C are not; two of three name someone she knows (A, C).

**D · The person pass: a housemate alone, in three versions.** It fires on arrival on the landing, in the hours his rows put him in his room (`npc_at_location` on his room), `chance = 0.35`, once a night. Each version shows behind the arc step that opens it; before that step it doesn't exist. Her choice in each is to watch or back away, and in release 1 each sets a flag only.

*D1, at the start: nothing about her* (41 words).
> His door is open a crack. He's on his bed with his jeans open and his phone held up, sound low, his hand working his cock fast.
> He hasn't seen you. The phone's what he's looking at.
> Your face goes hot.

*D2, after his first step toward her: her underwear* (39 words).
> The door's open again. He's on the bed, but there's no phone tonight. He has your black underwear from the laundry pile wrapped round his cock, and he's stroking slow.
> Your stomach drops. Those are yours. He took them.

*D3, near the top of his arc: her name* (36 words).
> His door's open wider than a crack tonight. He's working his cock hard, eyes shut, and he says it out loud, rough.
> "Fuck. Fuck, ___."
> Your name.
> Your breath catches. He left it open on purpose.

| button | the first line after the click (D1) |
|---|---|
| "Watch" | *He comes into his fist with a grunt and drops the phone on his chest.* · sets `saw_housemate_alone` |
| "Back away" | *You ease back down the landing, and the floorboard doesn't give you away.* |

## When someone walks in on her

The other kind needs more than a place and a window: it rides on an act she is doing, it lands on her body, and two of them on one act compete for the same moment.

1. **The act comes first.** The walk-in is a rule on the act's own canvas (`[[canvases.trigger.substitutions]]`, v2.py:14722-14738), so the act's piece is built before the walk-in's card. The card names that act and the piece that built it. If the act isn't built, the walk-in waits.
2. **Her body at the interruption.** She is mid-act: wet in the shower, half into a dress. That makes it a body moment too, so `craft/body-moments.md` applies in full. Her picture goes right after the line where he sees her, and it is her, at her tier, pool 4 on a repeat (C1262, C1280).
3. **He comes from his own row, still doing it** (L97, shape step 6). He has a reason to open the door that is about him: his razor, the bin, a towel. At the start of his arc the look is an accident; what it means to him moves only with his arc (shape step 13).
4. **Her buttons: two answers, cover or carry on.** One keeps her covered ("Cover up", "Pull it shut"), and one carries on with the act ("Keep washing", "Finish changing"). Each has its own line of his reaction after the click, and each sets its own flag, so a later step of his arc can tell them apart. That flag is the door: being caught opens his next step when that step exists (C302), and never skips past it (C174). In release 1 the flags are all it pays.
5. **Two walk-ins on one act share one roll.** Independent rules roll in order, and the first hit wins (v2.py:7047-7054), so the first rule shadows the second, and the order on the page decides who shows up. Put two walk-ins on one act in one `exclusive_group`: one roll, each walk-in keeps its own chance, and the chances add up to the total. If the roll lands on a walk-in whose conditions fail (he isn't in his room), the act plays plain, and the other walk-in doesn't get that roll (v2.py:7040-7041). A failed group slot also skips any independent rules on the same act, because the check returns there. Keep the group's sum at or under 1.

**F · Someone walks in on her, two walkers on one act** (40 words). Roles: a housemate and the landlady, both on her act "Take a shower" in the shared bathroom. The housemate comes from his bedroom row, mornings; the landlady from her landing row, with clean towels. One group: 0.20 for him, 0.15 for her, so the shower plays plain at least 65% of the time (more when one of them is out of their row).

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "shower_housemate_razor"
chance = 0.20
exclusive_group = "shower_walk_ins"

[canvases.trigger.substitutions.conditions]
version = "1.0"
logic = "AND"

[[canvases.trigger.substitutions.conditions.items]]
type = "npc_at_location"
location_id = "housemate_bedroom"
npc_id = "npc_housemate"
operator = "is_present"

[[canvases.trigger.substitutions]]
target_canvas_id = "shower_landlady_towels"
chance = 0.15
exclusive_group = "shower_walk_ins"
# its own npc_at_location condition, for the landing
```

> You're under the water with your eyes shut, soap sliding down your tits, when the door bangs open. The housemate, toothbrush in his mouth, half asleep.

Picture: *Her, 19, in a small shared bathroom shower, wet and bare, turning toward the door. gif.* `_t4`, pool 4.

> He stares one second. Then he looks hard at the sink. "Shit. My razor."

| button | the first line after the click |
|---|---|
| "Cover up" | *You cross an arm over your tits and turn to the tiles. "Sorry. Sorry." The door clicks shut.* · sets `housemate_razor_covered` |
| "Keep washing" | *You tip your head back and let the water run. He grabs the razor without looking up and pulls the door shut hard.* · sets `housemate_razor_kept_washing` |

Two screens: the moment, then the answer (C792). No meter moves.

## When someone comes to her

Kind (b). She arrives, and before the place's screen a named person is there for her: the neighbour waves her over, a classmate falls into step. The scene is the world reaching her, so it is written for that person and that place, never a stranger pulled from a pool.

Engine, cited. A random canvas at the place is rolled on every arrival (v2.py:6866-6986), after these filters: not when she comes back from a menu page (v2.py:6885), the place resting after a hit (`random_cooldown` arrivals, 3 by default, v2.py:6978-6983, 6936-6938), the canvas's schedule and conditions (`setup.isCanvasSelectable`, v2.py:6101), its `max_triggers_per_day` by name (v2.py:6913-6922), `entry_only_from` (v2.py:6924-6942), and `requires_npc` against the person's rows (v2.py:6948-6961). A story moment (a one-time canvas that is not random) goes first (v2.py:6056-6077, 6560-6566). Nothing in the engine limits these across places; the one-a-day brake is ours, a flag (author-game-v2 `references/engine.md` §7, §28).

1. **A named person, where they are** (C2186, L97). Two forms, and the check takes either:
   - **At her place:** `requires_npc` names them, and their rows put them at the place at that time.
   - **From next door:** they come to her from an adjoining place their rows put them in, a knock on her door, a call from the next room, a wave from the porch. The canvas has no `requires_npc` (it would ask for them at her place, v2.py:6948-6961) and gates on an `npc_at_location` `is_present` condition on the adjoining place (read at v2.py:5428-5444). Adjoining means the same area: a room sharing her place's `parent`, or that parent itself, the hub. The card names the place and why it adjoins. The scene's first line shows them arriving, and the reader judges it. Why: P49's approved "he knocks on her bedroom door" had his own room next door in his rows and no row in hers; the at-her-place form pushed it into the hall, a 13-minute window on weekdays, and lost the scene LO approved (LO, typed in main-lean 2026-11-26: "Go with your picks").
   Either way they arrive doing what their row has them doing.
2. **About half everyday.** Their life going on, a small social moment (C788, C802). Count the share across the release's scenes on the plan.
3. **One a day, across the game.** Every "comes to her" scene waits on the same flag (`is_false`), every choice on its first screen sets it, and `[engine.daily_tick]` clears it (C2187). A walk-in she comes across (kind a) and a story moment don't touch the flag; the check is red when a kind-(a) scene waits on it or sets it (C2195). `scripts/walkins.py` is red on a scene without it, on a way out that forgets it, and on two flags.
4. **Always a written way out** (C2188). Two choices at least, each with its own line after the click. While her meters are frozen a no is free; once feelings move, a no costs that person a little.
5. **A repeat rests or climbs** (C2189). **The rest is the game's number, and LO's call:** how many days before the same scene can come again goes on the plan with his words, never a default (`SKILL.md`, Always 8). Worked example: a game with about ten of these rests each scene three days, so no one scene crowds the week (LO's pick for such a game, typed in main-lean 2026-11-26: "Go with your picks"; measures: about a day in CoT, 4 to 10 days in Shady Deals after she takes the offer). Written as a `days_since_flag` condition on the scene's own flag, `operator = "gte"`, `value = 3`. Short of that rest: the same person not again for a day or more (`max_triggers_per_day = 1` and the brake give at most one a day; a longer rest is a `days_since_flag` condition on the flag its last visit set, `operator = "gte"`, read at v2.py:5208-5242; it fails while the flag was never set, so a first visit needs its own branch). Climbs: each step needs the one before (a flag the last step set). Never the same scene again at once.
6. **A story moment is never behind a chance** (C2190, C174). A person's arc step at a place is a one-time canvas that fires when due; it is not `trigger_mode = "random"`. The check is red when a card's Does: puts "a person's arc step" on a random canvas.
7. **Bolder answers by her level** (C2191), once meters move: a band on her level adds a choice. Release 1 has none.
8. **Release 1** (C2192): 8 to 10 of these, and the first steps of two or three chains, each setting a flag only.
9. **It fits what she is doing** (C2196). Before the card, answer: *what is she doing and wearing when this fires?* On arrival the answer is "she has just walked in, in whatever she had on": a wave, a word at the door, someone falling into step, a knock. When the words need her in the middle of an act (on the bench, at the table, at a desk with her books, under the water), the scene rides on that act instead:
   - The act (the "Work out" button) gets a `[[canvases.trigger.substitutions]]` rule naming the scene, with its `chance` and the person's presence (`npc_at_location`) in the rule's conditions (read at v2.py:14819-14843). It runs at the top of the act's first screen, after the act's costs are charged (v2.py:17839-17851, the cost gate wraps the substitution check), so the day pass and the energy are paid and the act counts.
   - The scene is `substitution_only = true` (never a button, v2.py:15272-15275), keeps its own `trigger.location` (the act's place: `setup.getCanvasById` finds only canvases listed under a place, v2.py:4160-4174), and keeps the brake and the rest on its own trigger: the engine checks the target's conditions, `max_triggers_per_day` and `requires_npc` before it swaps (`isCanvasValid`, v2.py:6141-6161; `_tryRule`, v2.py:7021-7037).
   - Its first screen is the act and the person in it: the workout under way, then him. Its exits spend the act's time and return her where the act does.
   It is still kind (b): one named person, the shared one-a-day flag set on every way out, a written way out. `scripts/walkins.py` checks the same rules on it, and is red when a scene that fires on arrival says "your stance", "your set" and the like (a short list; the reader is the real check).

**G · Someone comes to her, everyday** (38 words). Roles: a neighbour whose morning row is the park path, 07:00–09:00.

```toml
[canvases.trigger]
location = "<park>"
trigger_mode = "random"
chance = 0.3
requires_npc = "<npc_neighbour>"
is_repeatable = true
max_triggers_per_day = 1

[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [{ type = "flag", subject = "player", flag_key = "came_to_her_today", operator = "is_false" }]

# [engine.daily_tick] flagEffects = [{ targetType = "player", flag = "came_to_her_today", op = "unset" }, ...]
```

> The neighbour's at the gate before you're through it, dog lead in one hand, a coffee in the other.
> "You're the one from number nine. You run?" He looks you up and down. "You should. Mornings, with us."

| button | the first line after the click |
|---|---|
| "Maybe tomorrow" | *"I'll hold you to that." The dog's already pulling him off.* · sets `came_to_her_today`, `neighbour_run_asked` |
| "I'm late, sorry" | *He shrugs and lets the dog have its way.* · sets `came_to_her_today` |

The next step of the chain waits on `neighbour_run_asked`, a day or more later (step 5).

## When she gets noticed

Kind (c). She arrives in something worth looking at, and a stranger looks: the guys at the bus stop, a jogger, two regulars between sets. It is CoT's way: its events are tagged with what they need to see on her (cleavage, a short skirt, no bra), and the picker refuses an event her outfit can't meet (CoT's `cot_40_events.js`, lines 137-160; 20 cleavage events, 14 skirt, 14 topless, `Great_Games_Study_20260926/round12_tease/cot.md`, line 37). CoT's place descriptions don't do this job (`craft/places.md` rule 1). Our design, after it (C2200; LO, typed in main-lean 2026-11-27: "Yes, we should align our place description to it. And for scenes like leggings ones, those should be walkins right??", "dont we need skill changes").

1. **It fires on arrival, behind a chance, once a day:** `trigger_mode = "random"`, `chance = 0.35`, `max_triggers_per_day = 1`, like kind (a). It is off the shared "comes to her" flag.
2. **Only in the clothes it is about.** Its trigger's conditions name what she wears (`clothing_item`, `clothing_slot`, `worn_exposure` or `worn_type`), and the hours when people are about. The scene names only that garment (`craft/clothes.md` rule 4).
3. **A stranger is fine.** No named person and no schedule row are needed; a stranger speaks as `speaker = "unknown"`. A named person is allowed only where their rows put them (L97).
4. **Two screens, and a written way out** (C792, C2188): the moment, then one answer screen per choice. One choice is plain ("Keep walking"); one stays in it ("Look back", "Let him look").
5. **On her body, short.** What he looks at, what it does to her (face hot, walking faster), one spoken line from him. In release 1 it sets a flag only.
6. **Not too many** (L147: "69 of first_term's 82 random scenes were about her body"). At most a quarter of the game's arrival scenes are this kind, and at most one per garment state per place. `scripts/walkins.py` counts it.

**H · She gets noticed** (roles): her street, 07:00–21:00, in leggings.

```toml
[canvases.trigger]
location = "<street>"
trigger_mode = "random"
chance = 0.35
is_repeatable = true
max_triggers_per_day = 1

[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [{ type = "clothing_item", item_id = "leggings", operator = "equipped" },
         { type = "time_of_day", start_time = "07:00", end_time = "21:00" }]
```

> The guys at the bus stop go quiet as you pass. One of them whistles, low, and his eyes stay on your ass in the leggings.
> "Don't walk so fast, sweetheart."
> Your face goes hot.

| button | the first line after the click |
|---|---|
| "Keep walking" | *You don't look back. You can feel them watching until the corner.* · sets `noticed_<street>_leggings` |
| "Look back" | *He grins when you do. You turn away first, and your face burns.* · sets `noticed_<street>_leggings` |

## How a walk-in grows

(LO, relayed 2026-11-22: "does walkins progresses?? like she can do more in those walkins as things rises?? In the release 1 it stays basic obv. But how does top games do it??")

Engine, cited:
- A substitution rule's `conditions` are checked before its own dice: `_tryRule` first, then `Math.random() < chance` (v2.py:7081-7088). Rules with disjoint meter ranges are bands, each with its own chance.
- Rules sharing an `exclusive_group` share one roll in cumulative slots, and a claimed slot whose conditions fail falls to the plain act, not to the next rule (v2.py:7003-7008, 6968-6987). So bands go as independent rules; when an act already has a group, a new rule goes last in it (C1864). The chances in one group share one roll, so together they must stay at or under 1: bands of 0.10, 0.35 and 0.70 in one group add up to 1.15, and the last band gets only 0.55.
- `substitution_only = true` keeps the branch canvas out of the place's buttons (v2.py:15164-15167). The payoff canvas must have a `trigger.location`: `setup.getCanvasById` finds only canvases listed under a location (v2.py:4158-4171), so a payoff with none never fires and nothing says so (`.claude/skills/author-game-v2/references/the-surfaces.md:282-285`).

1. **Two sides grow.** His version moves with his arc (shape step 13). What she can do moves with her meter, up the kind's ladder (`.claude/skills/author-game-v2/references/the-heat-ladder.md` H3): overhearing goes hear, listen, look, touch, one button per rung; peek or catch adds an option each stage; an accident becomes her choice.
2. **One canvas, banded on her meter.** The bottom band is release 1. Build release 1's walk-in as that one canvas with its one band, so a later release adds a band and never rewrites the scene (C1820, C1821).
3. **The odds climb with the same meter as the content.** Low band rare, top band likely (0.10 / 0.35 / 0.70, C1820). A flat chance is listed on the card as a choice (C724).
4. **Two screens at most:** the moment, then one answer screen per choice (C792).
5. **Caught becomes a door.** Being caught can open his arc's next step (C302). It never skips past that step (C174).
6. **Release 1 is the bottom band only:** a flag, no meter. When meters move, a meter's first gain is never behind the dice (L70).
7. **Count her states.** Across a game, at least three of her states open new scenes or bands (C857).

**E · One walk-in in three bands** (overhearing; roles: a housemate in the next room). The router is on her act "Go to bed", while his rows put him in his room. Three rules on the same canvas, each with its own meter range and chance; only the bottom one exists in release 1.

| band | her meter | chance | the moment (one line) | her new choice |
|---|---|---|---|---|
| hear | under 20 | 0.10 | *Through the wall: his headboard, a girl's moan, his voice low.* | turn the music up, or lie still and hear it |
| listen | 20–39 | 0.35 | *You put your ear to the wall. You can hear what he's telling her to do.* | adds: press closer |
| look | 40 and up | 0.70 | *His door's open a crack, and from the landing you can see all of it.* | adds: stay where he might see you, the "caught" door into his arc |

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "wall_housemate"
chance = 0.10

[canvases.trigger.substitutions.conditions]
version = "1.0"
logic = "AND"

[[canvases.trigger.substitutions.conditions.items]]
type = "trait"
subject = "player"
trait_key = "<her meter>"
operator = "lt"
value = 20
```

A later release appends the 0.35 and 0.70 rules with their ranges and adds their bands to `wall_housemate`; the hear band's text stays as it was.

## Not this

- A place's description that notices what she wears ("…a neighbour's eyes drop to your chest in Mom's top"). The same words every visit, and no choice. It is a "she gets noticed" scene (C2200, C2201).

- An area where every scene is about her body. About half are everyday: someone else's life going on (L147; C802).
- "You walk through the park. Nothing happens." No scene at all is better (L150).
- Ten random events because a random-event helper already exists. Start from the study's share and do the math (L4).
- A walk-in whose window is a guess, or that shows him doing something his rows don't have him doing. He arrives from his own row, mid-task (L97).
- A meter's first point behind a 1-in-4 roll. The first gain is open without dice; chance only repeats it (L70).
- A person's next step left to the dice. It fires the first time it can (C174, C212).
- A scene with one button. She can always leave, and leaving has its line.
- A walk-in rewritten each release. It's one canvas; a release adds a band (C1820).
- The same chance at every meter level. The odds climb with the content (C724).
- A third screen after the answer (C792).
- A walk-in on an act that isn't built yet. The act's piece comes first.
- Someone walks in on her and the picture is the door, the steam or him. The picture is her, right after he sees her (C1262).
- Two walk-ins on one act as independent rules. The first one shadows the second; put them in one `exclusive_group`.
- A housemate who wants her in his first walk-in because his end want says so. His first one is about him, not her; she comes into it only as his arc moves (LO, 2026-11-21).
- A "comes to her" scene with no named person, or at a place their rows never reach, at hers or next door (C2186).
- A scene moved out of the room LO approved to fit a row, when the person comes to her from next door. Gate on the adjoining place instead (C2186, P49).
- Two of them in one day, because each place has its own rest. One brake flag covers the game (C2187).
- A scene that comes to her and leaves no way out, or a no that costs her while meters are frozen (C2188).
- A person's next step behind a 1-in-3 roll on arrival. It fires when due (C2190).
- A walk-in she comes across left as a button at the place. It fires on arrival (C2195). A button "by chance" doesn't exist either (v2.py:6488 is called from nowhere).
- A walk-in she comes across on the shared "comes to her" flag. That flag is kind (b)'s; kind (a) is once a day on its own (C2195).
- A scene that comes to her on arrival with words about an act she isn't doing yet: fixing her squat as she walks into the gym, sliding into the chair beside her as she comes through the library door. It rides on the act (C2196).
- Walk-ins found only by going place by place. Ask what each person does when alone, too, or the best ones turn up only by luck.
