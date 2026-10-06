# The Want — First Term

> One page, five parts. Doctrine: `references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.
> Premise picked by LO 2026-10-02: **taboo at home** — the house is the centre; college, the job and
> the neighbourhood feed it, because what happens outside comes home with her.
> This page is the starting core, not a closed list: people and places grow at the idea page, the
> spine's cast page, the board, and every release after (LO, 2026-10-02).

---

## 1. Who she is

Ella is 18, and the game says so on day one. Today is her first day of college. She still lives at
home in a rented house with her mom Laura, her step-father Mark and her step-brother Ryan. She has
never had a job, her own money or a lock on her door.

**The places she knows:**

- Home: the hall, the kitchen, the living room, the master bedroom (Laura and Mark's), her bedroom,
  Ryan's room, the shared bathroom.
- The neighbourhood: her street, Mr. Vance's house next door, the corner shop, the park she walks
  through to campus.
- Campus: the lecture hall, the library, the quad.
- The café near campus, and Zoe's apartment.

**What she has to lose:** her mom's trust, and how the house sees her.

**The player:** `female` · `written` (Ella; the name can be changed). Start choice, asked on day
one by the scene itself: *what do you want from college?* — good grades, fun, or freedom. Each
answer sets a flag that later scenes read. A memory, never a stat screen.

## 2. What holds her

The family rents the house from Mr. Vance for $1,200 a month. Now that she is 18, Mark says she
pays her cut: a quarter, **$75 every Sunday**, counted out on the kitchen table. Short means Mark
decides what happens next. Behind Mark stands Vance, who owns the house and lives next door, and
who comes knocking when the family is late.

**Hold kind:** `bill` · **collector:** Mark. Numbers here are placeholders until the board sets them.

## 3. What she wants

To be wanted by the people she shouldn't want. That never finishes; it is where she lands, not
where she starts.

**The goal that pulls the player:** pay her own way: earn enough of her own money that Sunday
rent is paid her way, not Mark's. Rent never stops; the goal ends the day she, not Mark, sets how
it is paid. When it is met, the next goal opens: her name on campus (the chain is on the idea
page).

**The charge:** taboo first (the house and the family in it), transformation on top (who she
turns into).

## 4. How she climbs

**Early:** flirting across the café counter for tips; Ryan catching her in a towel outside the
bathroom; a kiss at a campus party; her mom almost noticing.

**Late:** Ryan in her room while her mom is downstairs; Laura and Ella closer than a mother and
daughter should be; Sunday rent paid her own way; café regulars paying for more; Dr. Hale's office
after hours; Vance's porch when the family is short.

No numbers here. Tiers and rung values are set on the board.

## 5. The people and her life

Everyone is 18 or older, and the game says so.

| person | age | what she wants from them | what they visibly want, each visit | what they keep score of |
|---|---|---|---|---|
| `npc_ryan` — step-brother | 22 | the one person at home on her side | her, and he stops hiding it | want + warmth |
| `npc_mark` — step-father | 46 | his approval, and to be off the hook | control, and her | want + power |
| `npc_laura` — mom | 41 | to stay her good girl, and to be close to her | a happy house; she watches everything, and she wants Ella nearer than she says | want + warmth |
| `npc_zoe` — college friend | 19 | someone to follow into fun | a partner in trouble | step counter + memory flags |
| `npc_tom` — café manager | 31 | shifts and good tips | her behind the counter, closing late | want + power |
| `npc_hale` — professor | 39 | a passing grade | to see how far she will go | step counter + memory flags |
| `npc_vance` — owns the house, next door | 54 | for the rent to come in, every month | her, a little more each time she walks past his porch | want + power |
| `npc_jake` — campus guy | 20 | a normal boyfriend | a girlfriend he can show off | step counter + memory flags |
| `npc_nadia` — second-year student | 20 | the classmate who knows Hale's history and saves her a seat | to see whether Hale does to Ella what he did to her | step counter + memory flags |

**Roles:** Ryan is the main taboo. Mark is the pressure, and turns sexual late. Laura climbs.
Zoe is the companion, one step ahead of Ella.

**Her life — five threads besides home:**

| thread | person | place | system that runs it | its link into the hook |
|---|---|---|---|---|
| `college` | `npc_hale` | `campus` | college (lectures, grades) | her grades go home to Laura |
| `job` | `npc_tom` | `cafe` | job (shifts, tips) | it pays her cut of the rent |
| `friends` | `npc_zoe` | `zoe_apartment` | parties | what she brings home late |
| `dating` | `npc_jake` | `campus` | none — Jake's Saturday dates, booked on his phone thread (not a system, `SYSTEMS.md` §12, LO 2026-10-07) | Ryan sees |
| `neighbourhood` | `npc_vance` | `vance_house` | money pressure | her $75 is part of what Mark owes him |

---

## Before you leave this page

1. What can she reach at the top that she cannot at the bottom? Ryan's bed, Laura's trust used
   the other way, Mark's rent paid her own way, Vance's porch, the professor's office.
2. Which person would a player miss if deleted, and what does he want back? Ryan — her, and the
   one person in the house on her side.
3. Vocabulary check: `python3 scripts/gates.py --words games/first_term/WANT.md`.
