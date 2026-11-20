# PLAN: First Term (first_term_lean)

> The one-page game plan. Built from `WANT.md` and `IDEA.md` (LO keeps both as they are).
> Shown to LO in bites; each answer is a line in `NOTES.md`.

## 1. Her

Ella, 18, and the game says so on day one. Today is her first day of college. She lives at home in a
rented house with her mom Laura, her step-father Mark and her step-brother Ryan. No job, no money of
her own. Her old bedroom key is the one thing that's hers.

- **The player:** female, a written character (Ella). (WANT §1)
- **Name screen, two fields:** her name (default *Ella*) and what Ryan calls her (default *El*).
  Both are printed back in scenes, never used as gates. (IDEA §3)
- **Start choice, asked by the first scene:** what does she want from college: good grades, fun, or
  freedom. Sets one flag that later scenes read. A memory, never a stat screen. (WANT §1)
- **What she has to lose:** her mom's trust, and how the house sees her. (WANT §1)
- **Her face:** open.

Craft: C39, C42, C44, C46, C48, C49, C51, C54

## 2. The want

- **The hold:** a bill, collected by Mark. The family rents the house from Mr. Vance, next door.
  Her cut is due every Sunday: $75, then $90 after $300 paid, then $100 after $900, then flat.
  Short means Mark decides what happens next; behind him, Vance comes knocking when the family is late.
- **Goal 1, pay her own way:** ends on four Sundays in a row paid in full from her own money, or by
  the body route (taking Mark's chair at the top of his arc). Flag `pays_her_own_way`. Next: goal 2.
- **Goal 2, her name on campus:** her campus talk opens the party everyone goes to; she hosts it,
  and that scene sets the end flag. Next: goal 3.
- **Goal 3, beyond campus:** a man from town sits at Sunday dinner with the whole family, invited by
  Laura or Mark, who don't know what he is to her. Next: to be named.
- **The rival:** a classmate, 21, who can report her to the dean. No mystery.
- **The appetite (never finishes):** to be wanted by the people she shouldn't want. Where she
  lands, not where she starts.
- **The charge:** taboo first (the house), transformation on top (who she turns into).
- **The moments promised:** being seen, taboo at home, consequences she lives with. Her firsts
  mostly happen outside and come home with her.
- **The ascent, as doors:** at the bottom, the café counter, the towel in the hall, a party kiss.
  At the top, Ryan's bed, Laura's trust used the other way, Mark's rent paid her own way, Vance's
  porch, Hale's office after hours.

Craft: C28, C33, C35, C36, C37, C38, C55, C58, C60, C63, C65, C68

## 3. The people

Everyone is 18 or over, and the game says so.

| person | who | age | what she wants from them | what they want, every visit | keeps score of |
|---|---|---|---|---|---|
| Ryan | step-brother, main taboo | 22 | the one person at home on her side | her, and he stops hiding it | want + warmth |
| Mark | step-father, the pressure | 46 | his approval, and to be off the hook | control, and her (turns sexual late) | want + power |
| Laura | mom, climbs | 41 | to tell her everything, to be close | a happy house; wants her nearer than she says | warmth |
| Zoe | college friend, companion one step ahead | 19 | someone to follow into fun | a partner in trouble | steps + memory flags |
| Tom | café manager | 31 | shifts and good tips | her behind the counter, closing late | want + power |
| Dr. Hale | professor | 39 | a passing grade | to see how far she'll go | steps + memory flags |
| Mr. Vance | owns the house, next door | 54 | the rent to come in | her, a little more each time she passes his porch | want + power |
| Jake | campus guy | 20 | a normal boyfriend | a girlfriend he can show off | steps + memory flags |
| Nadia | second-year, retaking Hale's course | 20 | the classmate who knows Hale's history | to see if Hale does to her what he did to Nadia | steps + memory flags |
| the rival | classmate | 21 | (name open) | to beat her; can report her to the dean | steps + memory flags |

- **Arrivals come in waves, not all in week one.** Day one: the house, then Hale and Nadia. First
  week: Zoe, then Tom when she looks for work. First Sunday: Vance. Later: Jake, then the rival.
- **No one is named before she meets them.** Until then it's "the man next door", "a guy on the quad".

Craft: C567, C584, C606, C608, C610, C618, C628, C631, C650, C651, C657
Lessons: L93 (release 1 met all 10 people, 8 in week one), L115 (named before met)

## 4. The places

Map shape: nested zones (zone, then place, then room). The house is her hub; the outside is what
makes it risky.

| zone | places | kind |
|---|---|---|
| Home | the hall (hub, and the way out to her street; anything at the front door plays here) · kitchen · living room · shared bathroom · her bedroom (her old key locks it) · Ryan's room · the master bedroom (Laura and Mark's) | anchor |
| Neighbourhood | her street (passes through only) · Mr. Vance's house and porch, next door · the corner shop · the park (walk, rest, run; not her way to campus) · the gym | satellite |
| Campus | the quad (hub) · the lecture hall · the library · the cafeteria · the professors' offices (a corridor; Dr. Hale's is one door) · the dean's office (later) · a women's bathroom off the lecture-hall corridor · the theatre (drama studio) | satellite |
| Near campus | the café · Zoe's apartment | satellite |

- Every place says in its own text what it is and what she can do there.
- A room's menu holds only needs, systems and people.
- A closed place shows its hours and a closed line.
- Every one of these exists in release 1, shallow.

Decided:
- Getting to campus, both ways: bus $2 and 20 minutes; walk 45 minutes and some energy (placeholder
  numbers). Engine: a place's `entry_costs` take `time` plus any trait (`v2.py:6200-6203`).
- Hours: lectures weekdays 9–1, library 8am–10pm, café 7am–9pm, shop 7am–11pm, park 6am–9pm, gym 6am–10pm.
- Courses: Intro to Psychology (Dr. Hale), English Composition (Prof. Diane Walsh, 48, her advisor),
  Statistics (Mr. Owen Pratt, 44), Drama (Mr. Julian Cross, 38, basic in release 1). Dean Paul Sterling, 58.

Craft: C737, C738, C739, C761, C769, C776, C808, C809, C810, C811
Lessons: L33 (the house layout was a guess), L39 (the door has to be on the way home)

## 5. People, place by place

### Home

| room | face | other named people | crowd | who notices her, and what |
|---|---|---|---|---|
| the hall | none: everyone passes | Mr. Vance at the door when rent is late | none | Laura: when she comes home, and what she's wearing |
| the kitchen | Laura | Mark at the table on Sundays (rent) | none | Laura: her mood, her grades. Mark: her money |
| the living room | Mark (his chair, the TV) | Ryan on the couch | none | Mark: who she texts, what she's wearing |
| the shared bathroom | Ryan (the mornings) | none | none | Ryan: her in a towel |
| her bedroom | none: it's hers, the key | Laura knocks; Ryan at the doorframe | none | whoever knocks |
| Ryan's room | Ryan | none | none | none |
| the master bedroom | Laura and Mark | none | none | none: she shouldn't be in there |

Gaps:
- No one from outside comes into the house except Vance.
- There is no home crowd at all.

Decided (LO, yes): visitors are cast already named, Zoe staying over and Jake at the door (in the hall),
both in release 2 (LO's pick A); Mark's friends later. The master bedroom gets Laura's wardrobe, where she borrows clothes.

### Neighbourhood

| place | face | other named people | crowd | who notices her, and what |
|---|---|---|---|---|
| her street | none: passes through, the bus stop | Vance on his porch, Jake picking her up | neighbours, the bus queue | neighbours: what she wears out, and they tell Laura |
| Vance's house and porch | Mr. Vance | none | none | Vance: her, every time she walks past |
| the corner shop | Frank Novak (52, owner, days; knows Mark) | Danny Price (23, night clerk) | customers | Frank: what she buys, and he tells Mark. Danny: her, at night |
| the park | none | Zoe on a run (later) | joggers, dog walkers | joggers: her in running clothes |
| the gym | Marco Silva (29, trainer) | none | the regulars | the regulars: her body, her outfit |

### Campus

| place | face | other named people | crowd | who notices her, and what |
|---|---|---|---|---|
| the quad (hub) | Zoe | Jake and his friends | students between classes | the students: who she's with |
| the lecture hall | Dr. Hale (psychology), Mr. Pratt (statistics) | Nadia saves her a seat; Brooke | the class | Hale: her. Nadia: Hale looking. Pratt: if she's missing |
| the library | Ms. Ivy Holt (31, librarian) | Nadia studying | students studying | the face: who she studies with, and when |
| the cafeteria | Rosa Diaz (45, lunch lady) | Zoe, Jake, Brooke | the lunch crowd | the lunch crowd: who she sits with |
| the professors' offices | Prof. Walsh (her advisor) | Hale, Pratt and Cross, each behind his own door | none | Walsh: her grades, and she calls Laura |
| the dean's office (later) | Dean Sterling | Brooke, when she reports her | none | Sterling: what Brooke tells him |
| the women's bathroom | none | Brooke at the mirror | girls at the mirror | the girls: her outfit, and they talk |
| the theatre (drama studio) | Mr. Cross | Brooke, for the same part | the drama class | Cross: her under the lights |

### Near campus

| place | face | other named people | crowd | who notices her, and what |
|---|---|---|---|---|
| the café | Tom (manager) | Chris Dale (24, barista; wants her shifts, and her) | the regulars | Tom: her tips, her closing late. The regulars: her flirting |
| Zoe's apartment | Zoe | Sam Reed (22, Zoe's on-and-off boyfriend, always home) | none in release 1 (parties later) | the roommate: what she does there |

## 6. Rough arcs

Shape: each arc is a ladder of one-time steps. Its first third has no sex, and it ends by turning
into a repeatable sex scene. The central people get long chains (8 to 15 steps over weeks); the rest
get short ones. The opening steps teach two things: when this person is alone, and what they're
vulnerable about.

### 6a. Home

| person | chain | starts | middle | top |
|---|---|---|---|---|
| Ryan (main taboo) | long | he looks: the towel in the hall, first morning | he stops hiding it; she lets him look; the line moves | Ryan in her room while Laura is down the hall |
| Mark (pressure) | long, sexual late | Sunday rent at the kitchen table; short means he decides | what short costs grows: what she wears to pay, standing while he counts | the body route of goal 1: she takes his chair, and she sets the terms |
| Laura (climbs) | long | she almost notices: the hall, the late nights, the clothes | she talks to Ella like a friend; secrets both ways | closer than a mother and daughter should be; her trust, used the other way |

Decided (LO, yes): all three long; release 1 gives each only step 1, the first meeting.

### 6b. Outside

| person | chain | starts | middle | top |
|---|---|---|---|---|
| Zoe (companion) | medium | the quad, first week: she pulls Ella into fun | parties, a dare, Zoe one step ahead | Zoe and Ella together, a shared night |
| Dr. Hale | long | he watches her on day one; Nadia sees it | office hours, her grade, "how far will you go" | his office after hours |
| Tom | medium | she asks for work; her first shift | flirting for tips; closing late with him | café regulars paying for more |
| Mr. Vance | medium | first Sunday, the man on the porch | she walks past slower; the family is short and he knocks | his porch when the family is short |
| Jake | medium | a guy on the quad who asks her out | dates on Wednesday and Saturday; he shows her off | a normal boyfriend who doesn't know the rest; Ryan sees |
| Nadia | short | saves her a seat; "last spring it was me" | one line about Hale each lecture | what Hale did to her, told in full |
| Brooke (rival) | short | the classmate who wants the same part | the competition in drama and lectures | she reports Ella to the dean |

The other named faces (Walsh, Pratt, Cross, Sterling, Ivy, Rosa, Frank, Danny, Marco, Chris, Sam)
get no arc yet: in release 1 each one is met and is there. Short arcs come later, one release at a time.

## 7. What each release adds (rough)

Releases add steps, events and people at places that already exist, not new places (C76).

| release | adds |
|---|---|
| 1, the skeleton | every person, place and system; the daily loop; each person's first meeting, in waves; meters shown, none move yet |
| 2, the house | Ryan, Mark and Laura's next steps; Sunday rent with real costs when short; the meters start moving |
| 3, college and work | Hale and Nadia; Tom and tips; Zoe's first party; Jake's dates |
| 4, the street | Vance; goal 1 can end (four Sundays, or Mark's chair) |
| 5, her name on campus | goal 2 opens; Brooke's threat; the drama part |
| later | goal 3 (the man at Sunday dinner); short arcs for the named faces; past the top stages, who she does it in front of (WANT, release 41) |
