# [READY] System — meters
> Changed 2026-11-08 (DECISIONS 197): going out is Exhibitionism's alone; re-signed by LO 2026-11-08 ("Sign it").
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. File and line cites removed.

> **New 2026-11-01, signed by LO 2026-11-01** ("Signed", DECISIONS 113). Written from `proposals/R1_SYSTEM_METERS.md` (signed by
> LO 2026-11-01, "Signed."). It changes the meter rules of DECISIONS 78 and the street-door rows of
> `sheets/systems/wardrobe.md` (that sheet points here). Nothing new is decided here.

| row | answer |
|---|---|
| id · name | `meters` · Her two meters, working together |
| the two meters | **Corruption is what she does:** her nerve, her acts, her yes to a person. **Exhibitionism is what she shows:** her clothes, her body, being seen. |
| stages | 20 / 40 / 60 (Curious · Bold · Hungry for Corruption; Daring · Showing · Watched for Exhibitionism) |
| caps | a meter pays only while she is under her stage cap (19, 39, 59: DECISIONS 78, only her choice pays) |
| feeds | Corruption, Exhibitionism, the named men's Lust |
| reads | Corruption, Exhibitionism, her clothing state |
| what measured it (2026-11-01) | of 106 effects that raise her meters, 3 raise both (43 only Corruption, 60 only Exhibitionism); of 207 conditions that read them, 27 read both. Wearing it out paid nothing |
| source | LO (2026-10-31): "first to wear something short she need corruption, after that increases her corruption and exhibition both, learn how top games work on this matter." · CoT (`heat_study/p2_cot.md`) |

## Rule 1 · the first time out takes nerve

Going out in a level for the first time needs Corruption **or** Exhibitionism at that level.

| going out in | needs |
|---|---|
| a short skirt, or no bra | Exhibitionism 20 |
| no panties | Exhibitionism 40 |
| a towel, the sleep shirt, underwear, naked | never, this release (as built) |

- The door's message names the number: "Not in that skirt. Not yet. (Needs Exhibitionism 20.)" (DECISIONS 90).
- **Changed 2026-11-08 (DECISIONS 197):** what she shows out of the house is Exhibitionism's alone, as in Course of
  Temptation. Corruption no longer opens these doors. A drink still does, for that night, and pays nothing past her
  sober stage.

## Rule 2 · wearing it out raises both

- **Each day out in it** pays **Exhibitionism +1**, once a day (2026-11-08: it no longer pays Corruption, DECISIONS 197).
- Paid by a **street scene**, once a day: someone sees what she's wearing (Mr. Vance on his porch, a guy at the corner
  shop, a car slowing down). Its line changes by what she wears and her level.
- Build: one repeatable canvas on `street`, once a day (`out_shown_today` cleared in the daily tick), with a
  first-time-per-level flag that pays the Corruption +1.

## Rule 3 · an act raises the meter it uses

| the act | pays |
|---|---|
| she shows herself to someone, by choice (a flash, a towel slip, naked for Ryan) | Exhibitionism (+1 everyday, +3 a big first) **and** Corruption +1 |
| she does something with someone, unseen (a kiss, a handjob, sex behind a door) | Corruption only |
| she does something with someone, **seen** (Mark's radio in the next room, a party) | **both** |
| she touches herself alone | Corruption only |
| an accident (seen in the towel when she didn't choose it) | **nothing** (DECISIONS 78) |

## Rule 4 · mixed acts need both meters

An act that shows **and** is sexual with someone needs **both** stage numbers. Example: "Naked in his room" (Ryan,
Showing) stays Exhibitionism 40; the handjob under the blanket with Mark's radio next door needs Corruption 40 **and**
Exhibitionism 20. Each step sheet names which of its buttons are mixed.

## Rule 5 · one scene, buttons from both meters

Where a scene offers a yes, it offers **two kinds of yes plus the no**: a showing yes (by Exhibitionism) and a doing
yes (by Corruption). Example, Zoe's dare: "Flash them." (Daring) · "Kiss him." (Curious) · "Not tonight." Both go to
the same next screen with a different first line, as in CoT.

## Rule 6 · witnesses remember

When she shows herself by choice to a **named** man, his Lust +1 (most scenes already do, e.g. the towel slip). A
stranger's look pays nothing to anyone; it is the street scene's line.

## Against the taste columns

- **who sees:** the street scene gives every outfit a witness; rule 6 makes him remember.
- **how she says yes:** rule 5, two kinds of yes on the same screen.
- **what changes after:** both meters move, so her voice and her options change together.

## Rows a gate needs

| row | gate |
|---|---|
| the street door reads both meters | a meter is read |
| the street scene pays both, once a day | every clothing state is read |
| each step sheet names its mixed buttons | the numbers, the body and the clothes agree |

## Rule 7 · a new stage is a moment (2026-11-11, DECISIONS 229; signed by LO 2026-11-11, "Sign them")

> LO, 2026-11-11, on the study of how top games show her stages: "Yes c" (shorter stage cards, and a moment when she
> crosses a stage). The model is Cupid's Way: one pop-up per stage, with the stage's name, two or three lines about
> who she has become, and "new things open" (`cupids-way.txt:19980-20010`). It fires on the sidebar's morning check
> (`$time is 0`).

| row | answer |
|---|---|
| what | one short screen per stage, with the stage name as its title, 2–3 lines of who she is now, then what opens |
| where and when | her room, the first morning (06:00–11:00) after she crosses 20, 40 or 60, once per stage |
| pays | nothing, because she already crossed; it only says so |
| button | "Get up." (back to her room) |
| 80 | next release; the stage cards already say so |

**Built 2026-11-11, where the build differs:** her room is the wardrobe room, and nothing one-time may fire there on
entry (gate *nothing one-time at the shop or wardrobe*). So the moment comes from going to bed: the first night after she
crosses, "Go to bed" plays the stage's own sleep (`stages.py`, a substitution on `room_sleep`). Its bed line is the
stage's own, and its morning screen is the moment above. It sleeps her the same way the bed does. When two stages are due,
they come on two nights, Corruption first. The Showing line names her panties only while she wears them; bare, it
reads *"You stand at the mirror with nothing on, longer than you need to, and think about who you'd let see this. Then you
think about letting them."*

| stage | the moment | what opens (the stage card's own words) |
|---|---|---|
| **Curious** (Corruption 20) | You wake up thinking about it again: the couple in the park, a door left open at night. You used to look away. This morning you don't want to. | Watching, touching yourself, a kiss, a dare. |
| **Bold** (Corruption 40) | You lie with your hand flat on your stomach and you know it now. You'd let a hand stay. You'd put your mouth where you were asked to. | Hands, mouths, a price for a look. |
| **Hungry** (Corruption 60) | You wake up wet, and it isn't a dream. It's this house: your brother across the hall, Mark at the table downstairs. You want what you aren't allowed, and you want someone to see you take it. | The taboo at home, strangers who can see, a room watching. |
| **Daring** (Exhibitionism 20) | You pull on a top and leave the bra on the chair. Nobody told you to. You liked how they looked yesterday, and you want it again. | No bra, a short skirt out of the house, bigger tips at the café. |
| **Showing** (Exhibitionism 40) | You stand at the mirror in your panties longer than you need to, and think about who you'd let see this. Then you think about taking the panties off too. | No panties out, naked for someone you know, your feed. |
| **Watched** (Exhibitionism 60) | Being seen isn't enough now. You want to be watched: a room going quiet, a stranger who can't look away, and you not covering up. | A room watching, a stranger. |

## Not decided here

- Whether underwear-only goes out at Showing in a later release (home-only now).

## Why — the source of each key choice

| key choice | source |
|---|---|
| every rule on this sheet | `proposals/R1_SYSTEM_METERS.md`, signed by LO 2026-11-01 (DECISIONS 102) |
| caps 19 / 39 / 59, accidents pay nothing | DECISIONS 78 |
| name the number on a locked button | DECISIONS 90 |
