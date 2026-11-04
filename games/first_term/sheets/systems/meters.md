# [READY] System — meters
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
| a short skirt, or no bra | Corruption 20 **or** Exhibitionism 20 |
| no panties | Corruption 40 **or** Exhibitionism 40 |
| a towel, the sleep shirt, underwear, naked | never, this release (as built) |

- The door's message names both numbers: "Not in that skirt. Not yet. (Needs Corruption 20 or Exhibitionism 20.)"
  (DECISIONS 90: name the number).
- **Engine (no change):** each street-door rule gets a second `lt` item for
  Corruption, so it blocks only when **both** are under the level. AND of two items; no nested condition (B70).

## Rule 2 · wearing it out raises both

- **The first day out in each level** pays Corruption +1 **and** Exhibitionism +1. After that, each day out in it pays
  **Exhibitionism +1**, once a day.
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

## Not decided here

- Whether underwear-only goes out at Showing in a later release (home-only now).

## Why — the source of each key choice

| key choice | source |
|---|---|
| every rule on this sheet | `proposals/R1_SYSTEM_METERS.md`, signed by LO 2026-11-01 (DECISIONS 102) |
| caps 19 / 39 / 59, accidents pay nothing | DECISIONS 78 |
| name the number on a locked button | DECISIONS 90 |
