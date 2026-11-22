# craft/walk-ins.md — what she walks into, and who walks in on her

Read this before you write a card for a scene that waits at a place: something she walks into (a couple behind the boathouse, a fight on the stairs), or someone who walks in on her in the middle of an act (a housemate at the bathroom door). The plan's walk-ins bite (`plan.md` §8) lists them, area by area; each area's scenes are one piece.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it.

| id | what it asks | the failure it stops |
|---|---|---|
| C788 | random scenes are people: about 45 words, half everyday, nearly half with a choice; who is there and what they want sets the tone | L147 |
| C802 | the world is more than her body: about half of the events are everyday life (65% early): other people's lives, small social moments | L147 |
| C678 | at least half of these scenes name a person she knows | — |
| C854 | count the pool once, and credit each scene to the system it belongs to | — (the count) |
| C855 | each scene is filtered by hours, who is here, what she wears, her meters, days since | — |
| C856 | about half carry a time window | — |
| C857 | the pool opens as she changes: at least 3 of her states open new scenes | — (later releases) |
| C858 | a place she visits several times a day needs many scenes, each spaced a day or more apart | — (later releases) |
| C859 | pure chance annoys; a scene can also take something, not only add | — |
| C28 | the taboo-at-home shape runs on walk-in risk: each housemate has at least one walk-in at home | — (the person pass) |
| C1820 | the odds ride the same meter as the content: chance bands 0.10 / 0.35 / 0.70 into one canvas banded watch / touch / act | — (how it grows) |
| C724 | walk-in odds read her climb; flat odds are listed | — |
| C1821 | three parts: the router (substitutions on the act), the branch (one `substitution_only` canvas with bands), the payoff (into a rung that exists) | — |
| C1864 | band with a rule's `conditions`; in an exclusive group, append a new rule last | — |
| C792 | a walk-in is two screens: the moment, and one answer screen per choice; a third screen is the defect | — |
| C302 | peek or catch: an option is added each stage, and being caught becomes a door | — |
| C212 | a story beat is never left to luck: it fires the first time it can | — |
| C174 | a person's next arc step comes before any dice | — |
| L97 | a walk-in only fires where the walker's rows put them, and it shows what they were already doing | first_term's walk-ins almost never fired; a TV walk-in swapped her film for its own |
| L70 | a meter's first gain is never behind a chance roll | first_term's Exhibitionism sat at 0 behind a 1-in-4 walk-in |
| L147 | the world felt empty: 69 of first_term's 82 random scenes were about her body | — |
| L150 | no "nothing happens" scene, anywhere | first_term had them; LO cut them all |
| L4 | plan from the study's answer and its target, not from the tools already built | first_term planned 10 random events because a helper existed, and reached 19% of ~50% |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **A scene she walks into** is a canvas whose `trigger.location` is the place. It shows as a button there. `max_triggers_per_day = 1` makes it once a day (read at v2.py:15060).
- **A scene behind a chance** sets `trigger_mode = "random"` and `chance` on its trigger (read at v2.py:15086-15089). The engine rolls each time the place's list is built, and on a miss the button is not there (v2.py:6404-6410).
- **Someone walks in on her** is a rule on the act she is doing: `[[canvases.trigger.substitutions]]` with `target_canvas_id`, `chance` and conditions (v2.py:14662-14672). `setup.checkAndSubstituteCanvas` (v2.py:6915) runs it when she starts the act; each rule rolls its own dice and the first that hits wins (v2.py:6987-6994). An `npc_at_location` condition reads the person's rows: `scripts/who_is_where.py` shows where the rows put them.

## The shape

1. **After the schedules.** A walk-in sits where a person's rows already put them, so the schedules come first (L97).
2. **Per area, per place:** one or two scenes. For each, say which kind it is: she walks in on something, or someone walks in on her.
3. **Who.** Half or more name a person she knows (C678). Strangers fill the rest.
4. **Everyday, about half.** A person doing their own thing, a small social moment, their life going on without her (C802, C788). The other half may be about her body or what she sees. Count the share across the area before the card, and write the count on the card (L4).
5. **Her choice.** Each scene asks her something. She watches or she leaves; she helps or she says she's late. Every button has its own line after the click, and leaving is written, not a silent exit.
6. **The window.** From the person's rows, not a guess. Someone walking in on her comes from their neighbouring row and is still doing it: the towel over his shoulder, the mug in his hand (L97). Never a second version of what they do.
7. **How often.** Once, or once a day. Say which on the card.
8. **What it pays.** While her meters are still (release 1), a scene sets a flag only and pays nothing. When meters move, a meter's first gain is never behind a chance roll (L70); a chance scene can repeat a gain, never be the first.
9. **Never empty.** No scene of "nothing happens" (L150). If a place has nothing, it gets no scene.
10. **The arc first.** If a person's next step is ready, it is its own scene with no chance on it, and the walk-ins with that person wait behind it (C174, C212).
11. **Seeing is not her sex.** Sex she sees or hears is a walk-in. Her own sex opens only with a partner (`plan.md` §10).
12. **The person pass.** Beside the place pass, take each person she lives with or sees often and ask: when this person is alone, what are they doing right now, at this point in their arc? Their rows give the where and the when. In a taboo-at-home game, each housemate has at least one walk-in at home (C28).
13. **The person now, not their end want.** A walk-in shows where the person is in their arc today. A person who wants her later does not want her in their first walk-in. A new version comes only when their arc moves a step, and each version is still what they were already doing (L97). (LO, relayed 2026-11-21: "in the starting ryan doesnt want her.")

## Worked example

Roles, not a world: a riverside park in her area, a neighbour she knows, two strangers, and a lodger at home. Word counts are for the story text.

**A · Everyday, a person she knows** (40 words). Button at the park, 07:00–10:00, while the neighbour's row puts him on the path. Once a day.
> The neighbour is on the bench by the gate, his dog's lead wrapped twice round his fist.
> "You. Hold him a minute? My laces." The dog is already pulling toward you.
> You blink. He's never asked you for anything before.

| button | the first line after the click |
|---|---|
| "Take the lead" | *The dog drags you two steps. He laughs, the first time you've heard it.* · sets `held_the_dog` |
| "Sorry, I'm late" | *"Course you are." He bends to his laces without looking up again.* |

**B · She walks in on something, strangers** (53 words). Button "Take the path under the bridge", 19:00–21:30. Once a day.
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

**D · The person pass: a housemate alone, in three versions.** A button "His door's open a crack" on the landing, in the hours his rows put him in his room, once a night. Each version shows behind the arc step that opens it; before that step it doesn't exist. Her choice in each is to watch or back away, and in release 1 each sets a flag only.

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

## How a walk-in grows

(LO, relayed 2026-11-22: "does walkins progresses?? like she can do more in those walkins as things rises?? In the release 1 it stays basic obv. But how does top games do it??")

Engine, cited:
- A substitution rule's `conditions` are checked before its own dice: `_tryRule` first, then `Math.random() < chance` (v2.py:6987-6994). Rules with disjoint meter ranges are bands, each with its own chance.
- Rules sharing an `exclusive_group` share one roll in cumulative slots, and a claimed slot whose conditions fail falls to the plain act, not to the next rule (v2.py:6909-6914, 6962-6981). So bands go as independent rules; when an act already has a group, a new rule goes last in it (C1864).
- `substitution_only = true` keeps the branch canvas out of the place's buttons (v2.py:15104-15107). The payoff canvas must have a `trigger.location`: `setup.getCanvasById` finds only canvases listed under a location (v2.py:4118-4131), so a payoff with none never fires and nothing says so (`.claude/skills/author-game-v2/references/the-surfaces.md:282-285`).

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
- A housemate who wants her in his first walk-in because his end want says so. His first one is about him, not her; she comes into it only as his arc moves (LO, 2026-11-21).
- Walk-ins found only by going place by place. Ask what each person does when alone, too, or the best ones turn up only by luck.
