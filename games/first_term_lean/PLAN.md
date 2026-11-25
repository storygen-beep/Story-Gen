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
- **Start choice, asked by the first scene:** who she was in high school, asked by Mom at breakfast on
  her first day ("promise me you'll still be the girl you were in high school"): the good girl, the
  party girl, or the one planning to get out. Sets one flag (start_grades / start_fun /
  start_freedom) that later scenes read. A memory, never a stat screen. (WANT §1; LO 2026-11-24)
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

| person | who | age | what she wants from them | what they want, every visit | feelings at the start (P48) |
|---|---|---|---|---|---|
| Ryan | step-brother, main taboo | 22 | the one person at home on her side | at the start: nothing from her · where he ends up: her, and he stops hiding it | friendship 0 · lust 100 · control 0 |
| Mark | step-father, the pressure | 46 | his approval, and to be off the hook | control, and her (turns sexual late) | 0 · 0 · 500 |
| Laura | mom, climbs | 41 | to tell her everything, to be close | a happy house; wants her nearer than she says | 300 · 0 · 200 |
| Zoe | college friend, companion one step ahead | 19 | someone to follow into fun | a partner in trouble | 250 · 0 · 100 |
| Tom | café manager | 31 | shifts and good tips | her behind the counter, closing late | 50 · 100 · 500 |
| Dr. Hale | professor | 39 | a passing grade | to see how far she'll go | 0 · 300 · 300 |
| Mr. Vance | owns the house, next door | 54 | the rent to come in | her, a little more each time she passes his porch | 100 · 400 · 400 |
| Jake | campus guy | 20 | a normal boyfriend | a girlfriend he can show off | 100 · 300 · 0 |
| Nadia | second-year, retaking Hale's course | 20 | the classmate who knows Hale's history | to see if Hale does to her what he did to Nadia | 200 · 0 · 0 |
| the rival | classmate | 21 | (name open) | to beat her; can report her to the dean | Brooke: -200 · 0 · 150 |

- **Arrivals come in waves, not all in week one.** Day one: the house, then Hale and Nadia. First
  week: Zoe, then Tom when she looks for work. First Sunday: Vance. Later: Jake, then the rival.
- **No one is named before she meets them.** Until then it's "the man next door", "a guy on the quad".

**The people system** (P48; LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Meter
frozen", "i say three", "Go ahead with your picks", "Yes to both A and B"). `[engine.people] system = "cot"`: every
person has friendship, lust and control on -1000..1000, gender, attracted, age, and 2–4 hidden trait words (P50); what they want
from her is worked out by the engine (none is hand-set). Release 1 moves none of it. Full per-person table, with the
line behind each trait: `cards/P48.md`.

| type | friendship | lust | control | trait words it draws from |
|---|---|---|---|---|
| Family, parent | 300 | 0 | 200 | Warm, Gives way, Strict, Takes charge, Cook |
| Family, sibling | 0 | 0 | 0 | Shy, Gives way, Gamer |
| Faculty (professor, intimacy 0) | 0 | 0 | 150 | Strict, Takes charge, Pushy, Warm, Sly, Bookish, Arty |
| Student | 0 | 0 | 0 | Warm, Pushy, Nervous, Gives way, No strings, Show-off, Arty |
| Worker (over her) | 50 | 0 | 250 | Pushy, Sly, Takes charge |
| Town (neighbours, shops) | 0 | 0 | 0 | Pushy, Takes charge, Watcher, Gossip, Sly, Show-off, Warm, Cook, Sporty |
| Rival | -150 | 0 | 0 | Mean, Pushy, Takes charge, Shy, Gives way |

The CoT trait names P48 first used are replaced by the game's own words below (P50).

### Trait words (P50; LO, typed in main-lean 2026-11-26: "Hide them dont show them, they are for us", "yes fine")
The game's own list, LO's call. The author's brief for each person's scenes; the player never sees them
(`show_traits = false`). Each is a row in `[engine.people.traits.<Word>]`; the sets and the node check are on
`cards/P50.md` (C2193, C2194).

| word | how they act |
|---|---|
| Pushy | Takes the lead with her, says what they want, doesn't wait to be asked. |
| Shy | Looks away, says little, waits for her to speak first. |
| Nervous | Unsure of themselves; asks for reassurance, second-guesses. |
| Warm | Looks after her: food, a seat, a warning; glad to see her. |
| Mean | Enjoys putting her down, best in front of others. |
| Strict | Rules, orders, checks up on her; things done their way. |
| Gossip | What she does gets told to someone, usually Mark. |
| Sly | Hides something, or takes what isn't theirs; a little underhand. |
| Takes charge | With her body, they lead and move her where they want her. |
| Gives way | Yields to whoever's stronger; follows, goes along. |
| No strings | Won't be tied to one person; nobody owns them. |
| Watcher | Their eyes are on her whenever she passes, and they don't hide it. |
| Show-off | Wants to be looked at: the party, the dress, the open door. |
| Gamer | Into games: the controller is where you find them and what they talk about. |
| Cook | Into cooking: the stove is where you find them and what they talk about. |
| Sporty | Into training: the gym is where you find them and what they talk about. |
| Bookish | Into books and numbers: their talk is the work. |
| Arty | Into making something: the stage, the guitar. |

Each person's words, with the line that shows each (C2193):
  Laura: Warm ("Sit with me a minute, baby."), Nervous ("Tell me one good thing. Just one."), Gives way (P38: "Then be
    quiet, Laura. Be quiet for me."), Cook ("Mom's at the stove.")
  Mark: Strict ("Straight A's don't pay rent."), Takes charge (P38, his hand over her mouth; "One way or another")
  Ryan: Shy ("Sorry. I didn't— Sorry.", his ears pink), Gives way (backs off every time), Gamer ("on the couch with a
    controller")
  Tom: Pushy ("Good answer. I'm Tom. I run the place."), Sly (P41, walk_tom_tips: "two of the bills fold into his own shirt pocket.")
  Chris: Pushy ("Entertain me. Go on, I'm bored."), Takes charge ("Tom says you're mine to train.")
  Dr. Hale: Takes charge ("Young lady. In here a minute."), Strict ("Either take notes or take a seat down here.")
  Mr. Pratt: Strict ("I take attendance, and I notice who isn't here."), Bookish ("fills three whiteboards with numbers")
  Prof. Walsh: Strict ("I read every word of it"), Warm ("I'd rather hear how you're doing from you"), Bookish (takes an
    essay apart line by line)
  Mr. Cross: Pushy ("Louder."), Takes charge ("makes you say the line three times"), Strict ("the same four lines, over
    and over"), Arty (runs the drama class)
  Ms. Holt: Strict ("No food, no phones, no noise."), Sly (the romance novel inside the library-science cover)
  Dean Sterling: Strict ("Dress like a student, not like a guest."), Takes charge ("Classes are not optional, child.")
  Nadia: Warm (saves the seat; "Trust me."), Pushy ("Sit here, freshman. Not the front."), Gives way ("Last spring it
    was me.")
  Zoe: Show-off ("Zoe throws these every week"; dancing "like the party's hers"), No strings ("Sam's not mine. Nobody's
    mine.")
  Sam: No strings (grins at "Nobody's mine"), Arty ("a guitar he can't play")
  Jake: Nervous ("With me, I mean." / "Okay. Okay, good."), Gives way ("my friends dared me")
  Brooke: Mean ("Did you get dressed in the dark?"), Pushy (opens on Ella in front of everyone), Takes charge (owns the
    mirror; "Cat got your tongue, princess?")
  Kayla: Mean ("Kayla laughs." at the insult), Gives way (holds Brooke's bag)
  Tess: Shy ("says less"; "Tess doesn't [laugh]"), Gives way (does Brooke's lashes)
  Mr. Vance: Pushy ("Come here a minute, little lady."), Takes charge ("I'm the one who knocks."), Watcher ("His eyes
    stay on your legs the whole time you answer.")
  Frank: Gossip ("Oh, I'll tell him you were in."), Watcher ("Everybody knows what everybody buys.")
  Danny: Pushy ("Hey, gorgeous."), Sly ("something small goes one way, a fold of notes the other")
  Marco: Takes charge ("Lower. Lower." and his hands on her hips), Show-off ("Look all you want. Everyone does."),
    Sporty (the trainer)
  Nina: Pushy ("Let me see. Come on, I won't tell."), Show-off ("in the shop's tightest black dress, turning to check her
    ass in the mirror")
  Rosa: Warm ("Here, take a roll."), Pushy ("Eat all of it. I'll know."), Cook (the counter)

Tuned after the readings (start values must agree with the scenes): Tom, Sam and Ryan start at lust 100, and Ms. Holt
is attracted with lust 100, each for a look on screen (Ryan's eyes on her chest, his ears pink: he hides it, so "at the
start: nothing from her" still holds). Mark stays at lust 0: his watching reads as control.

Craft: C2177, C2178, C567, C584, C606, C608, C610, C618, C628, C631, C650, C651, C657
Lessons: L93 (release 1 met all 10 people, 8 in week one), L115 (named before met)

## 4. The places

Map shape: nested zones (zone, then place, then room). The house is her hub; the outside is what
makes it risky.

| zone | places | kind |
|---|---|---|
| Home | the hall (hub, and the way out to her street; anything at the front door plays here) · kitchen · living room · shared bathroom · her bedroom (her old key locks it) · Ryan's room · the master bedroom (Laura and Mark's) | anchor |
| Neighbourhood | her street (passes through only) · Mr. Vance's house and porch, next door · the corner shop · the clothes shop (10am–7pm, closed Sundays) · the park (walk, rest, run; not her way to campus) · the gym | satellite |
| Campus | the quad (hub) · the lecture hall · the library · the cafeteria · the professors' offices (a corridor; Dr. Hale's is one door) · the dean's office (P47: his door on the corridor, his first-day scene in release 1) · a women's bathroom off the lecture-hall corridor · the theatre (drama studio) | satellite |
| Town (P45, LO 2026-11-25: "New Town hub") | the high street (hub; the bus stop, the campus gates, 5 minutes to the quad) · the café · Zoe's apartment | satellite |

- Every place says in its own text what it is and what she can do there.
- A room's menu holds only needs, systems and people.
- A closed place shows its hours and a closed line.
- Every one of these exists in release 1, shallow.

Decided:
- Getting to town, both ways (P45; was "to campus"): bus $2 and 20 minutes; walk 45 minutes, 10 energy there and
  none home (P04: she can always get home). Engine: a place's `entry_costs` take `time` plus any trait (`v2.py:6200-6203`).
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
| the clothes shop | Nina Kovac (26, runs it) | none | other shoppers | Nina: what she tries on, and what she buys |

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

### Town (was "Near campus", P45)

| the high street (Town) | none: passes through, the bus stop, the campus gates | none | students and shoppers | none in release 1 |

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
| 1, the skeleton | every person, place and system; the daily loop; each person's first meeting, in waves; people's feelings and her four skills shown, none move (P48) |
| 2, the house | Ryan, Mark and Laura's next steps; Sunday rent with real costs when short; feelings and skills start moving (people.md rule 15, meters.md) |
| 3, college and work | Hale and Nadia; Tom and tips; Zoe's first party; Jake's dates |
| 4, the street | Vance; goal 1's body route (Mark's chair); the four-Sundays end counts from release 1 (§8i; ENI's call, for LO to review, 2026-11-24) |
| 5, her name on campus | goal 2 opens; Brooke's threat; the drama part |
| later | goal 3 (the man at Sunday dinner); short arcs for the named faces; past the top stages, who she does it in front of (WANT, release 41) |

## 8. Systems, place by place (plan.md §6; added 2026-11-21 after the skill fix)

Rule: every open place has one thing she can do alone; "Nothing to do here right now" is never standing
text. Alone the click is plain; with a person it pays (C1340, L149). Every system usable on day 1 at
its bottom rung (C1462).

### 8a. Home life

| room | system | alone | with a person |
|---|---|---|---|
| Hall | routes only | none (it's the way through) | none |
| Kitchen | meals | Eat something (built, P06) · Do the dishes (chore) | Breakfast with the family at a set hour, mornings · Dinner with Laura, evenings · Sunday rent with Mark (P11) |
| Living Room | rest and TV | Watch TV (time passes, small energy back) | Sit with Ryan on the couch · Mark's chair (he's in it evenings) |
| Your Bedroom | sleep, study, clothes, phone | Sleep (built) · Study (college) · Change clothes (P07) · Lock your door (her key) | Laura knocks to talk (later) |
| Ryan's Room | his things | Borrow one of his hoodies (clothes) | Talk to Ryan |
| Master Bedroom | Laura's wardrobe | Borrow from Laura's wardrobe (P07) | none |
| Bathroom | body care (next bite) | Shower (built) | the shared bathroom: Ryan showers first (Laura's ruling at breakfast) |

Also from C1340: a "Wait" button in the house (pass 30 minutes), and a talk button per housemate.

Decided (LO, yes, 2026-11-21): talk and meal buttons in release 1 with a reaction line and no meter;
release 2 turns on the +1. Chores pay no money. Ryan's hoodie, yes.

### 8b. Body care

Energy is the one body need. Sources: sleep (to 100), a meal (+15), a shower (+5), TV (+5), a snack
(+10). Sinks: the walk to campus (10), class, shifts, the park, the gym.

| place | alone | with a person |
|---|---|---|
| Your Bedroom | Sleep (built) | none |
| Bathroom | Shower (built) | the shared bathroom; walk-ins in release 1 (P38, §10a) |
| Living Room | Watch TV (+5) | (home life) |
| Park | Go for a run (45 min, 15 energy): the run on screen, and who looks | none in release 1 |
| Gym | Work out (1 hour, 20 energy, $5 day pass) | Marco, at his meeting |
| Women's Bathroom (campus) | Fix your hair and make-up (10 min) | none |
| Corner Shop | Buy a snack ($2, +10) (money bite) | Frank or Danny at the till |

No hygiene meter and no arousal meter in release 1.

### 8c. Money

One currency, dollars ($). She starts at $0. No allowance: Laura's money stopped at college.

Income, release 1: the café only, after Tom hires her (P21). Shifts every day (8f): $5 an hour
plus a flat $2 tips, $22 a shift, said in the scene that offers the work, never on the button (C954).
Four shifts, or fifteen single hours, cover the $75 rent (any hour, 8f).

The bill: rent to Mark, every Sunday, on the rent page: $75, then $90 after $300 paid, then $100
after $900. Each week she trades shifts against class, study and people. What keeps it from going
soft (C946): the rent climbs, and from release 3 tips grow with her flirting.

Sinks (what money is for):
| sink | price | what it opens |
|---|---|---|
| rent | $75 a week | goal 1; short means Mark decides (release 2) |
| the bus | $2 each way | 25 minutes of her day back, and no energy spent |
| the gym day pass | $5 | Marco, and the workout |
| a snack, corner shop | $2 | +10 energy; Frank or Danny at the till |
| a coffee, café | $3 | +10 energy; Tom or Chris behind the counter, once she's worked her first shift and met both (P33 reader fix, ENI for LO 2026-11-24) |
| lunch, cafeteria | $4 | +15 energy; Rosa at the counter |
| clothes, the clothes shop | $10 to $30 | what she can wear where, and who notices |

| place | alone | with a person |
|---|---|---|
| Café | Buy a coffee ($3) · Work a shift (after P21) | Ask Tom for work (P21) |
| Corner Shop | Buy a snack ($2) | Frank or Danny at the till |
| Kitchen | The rent page, Sundays | Mark at the table (P11) |

No paid sex in release 1 (C967); the pay checks show n/a.

### 8d. Clothes

The engine's seven slots: bra, underwear, top, bottom, dress, legwear, shoes
(`apps/projects/services/template_import.py:278`). The world reads one number, how much she shows
(`worn_exposure`) (C1167).

What she owns, from the start: jeans, a T-shirt, a cardigan, a sundress, sneakers, a plain bra and
panties, pyjamas, leggings and a sports top. Laura's wardrobe, to borrow: a short skirt, a low-cut
top, heels. Ryan's room: one of his hoodies.

| place | alone | with a person |
|---|---|---|
| Your Bedroom | Change clothes (the outfit picker) | none |
| Master Bedroom | Borrow from Laura's wardrobe | Laura catching her at it (release 2) |
| Ryan's Room | Borrow one of his hoodies | Ryan seeing her in it (release 2) |

Rules:
- Leaving the house needs a top and a bottom, or a dress. The hall's "Exit Home" says why when it
  won't open: "You're not going out like this." (the standing rule: no public topless or bottomless).
- Ryan's hoodie with nothing under it counts as a dress at home only.
- The run and the workout need the leggings and sports top; the button says so.
- People notice, one line each, release 1: Laura in the hall when she goes out in Laura's things;
  the neighbours on her street; the girls at the campus mirror. No meter moves.
- Clothes to buy, release 1: the clothes shop on her street (LO "yes", 2026-11-21).
  Clothes Shop (Neighbourhood, off Your Street, 10am to 7pm, closed Sundays). Face: Nina Kovac,
  26, runs it; notices what she tries on. Crowd: other shoppers. Alone: Browse the rails (the
  catalogue, C780) · Try it on in the fitting room (the mirror; what she sees). With a person: Nina's
  one line at the till. Every item is a garment with a price over 0 (C1150).
  Stock, four levels per slot (LO 2026-11-21: "normal, sexy, super sexy, slutty"):

  | slot | normal | sexy | super sexy | slutty |
  |---|---|---|---|---|
  | top | plain tee $10 | crop top $12 | low-cut tank, no bra line $20 | sheer mesh top $30 |
  | bottom | jeans $25 | denim shorts $15 | tight mini skirt $25 | micro skirt $30 |
  | dress | summer dress $25 | tight black dress $30 | backless mini dress $45 | cut-out bodycon dress $60 |
  | bra | cotton bra $8 | lace bra $12 | push-up bra $20 | sheer bra $25 |
  | underwear | cotton briefs $5 | lace panties $8 | thong $12 | crotchless panties $20 |
  | legwear | tights $6 | thigh-high socks $10 | fishnets $15 | stockings and garter belt $25 |
  | shoes | flats $15 | ankle boots $25 | heels $35 | platform heels $45 |

  Every item is in the shop from release 1, with its price. Buying needs the money and the trait
  (LO 2026-11-21): normal needs nothing; sexy needs level 2, super sexy level 4, slutty level 6 (P48: the old 20 /
  40 / 60 on a 0–100 meter, ×10 on CoT's 0..1000 skills). What she shows (top, bottom, dress, legwear, shoes) reads
  Exhibitionism; what's under (bra, underwear) reads Disinhibition (was Corruption). Release 1 moves no skill, so only
  normal can be bought. A locked item shows "Needs Disinhibition 2" (a `skill_level` condition with locked_text,
  v2.py `_crLockReason`). Layout: `[ui] clothes_layout = "room"`, because the table layout's tiers are fixed at
  0/45/85/135 and read one fixed meter only (v2.py:2429-2434, 2464-2467).
  Gates and layout: LO "yes", 2026-11-21.
- The opening's "Get dressed" must put her day clothes on, or open the picker (C719, C1166).

### 8e. The phone

Release 1: Messages (chat) only (LO 2026-11-21). A person goes into her contacts when she meets
them. Each sends one text after the meeting, and she answers from two or three replies; a reaction
line back, no meter moves. Laura and Ryan are in it from the opening. No goals app: goal 1 stays on
the quest page. No phone credit: the phone is on Mark's family plan, and Mark sees who she texts.
Later: camera and gallery, the feed, calls, buying clothes online.

### 8f. College and work

Timetable, lectures weekdays 9–1 (PLAN §4):
| day | 9–11 | 11–1 |
|---|---|---|
| Mon, Wed | Intro to Psychology, Dr. Hale, lecture hall | Statistics, Mr. Pratt, lecture hall |
| Tue, Thu | English Composition, Prof. Walsh, lecture hall | Drama, Mr. Cross, theatre |
| Fri | no lectures | no lectures |

Grades: one meter, Grades, 0–100, shown as a letter (F under 40, D, C, B, A from 80). Starts at
50 (C). Readers: Walsh at office hours, Laura in the kitchen, the start choice "good grades".
Grades do not move in release 1 (LO 2026-11-21: "nope grades dont move in thius release"). Class
and study still show the act on screen (reader test 11); no line claims a grade changed.

Café work (after P21), every day, any hour Tom or Chris is behind the counter (LO 2026-11-24,
relayed by ENI: "shifts are independent of the classes, she can choose between things, its players
freedom"; was weekdays 2–6pm and weekend slots, LO 2026-11-21): "Work an hour" (1 hour, 4 energy,
$5) or "Work a shift" (4 hours, 15 energy, $22). Starts: an hour, weekdays 7am–7:55pm, Saturday
10am–7:55pm, Sunday 10am–6:55pm; a shift, weekdays 7am–4:55pm, Saturday and Sunday 10am–3:55pm
(Chris's weekend row ends at 8pm). LO 2026-11-24: shifts are independent of classes.
Pay (LO "A", 2026-11-21): $5 an hour plus $2 tips, $22 a shift, said in Tom's scene.
Four shifts, or fifteen single hours, cover the $75 rent (any hour, 8f). A missed shift costs only its
pay in release 1.

| place | alone | with a person |
|---|---|---|
| Lecture Hall | Go to class (2 hours, 10 energy, in its slot) · Study in an empty row (1 hour, 5 energy; added by ENI for LO, 2026-11-24) | Hale or Pratt teaching; Nadia saves her a seat |
| Theatre | Go to drama (2 hours, in its slot) · Practise on the empty stage (30 min) | Cross; Brooke |
| Library | Study (1 hour, 5 energy) | Ms. Holt at the desk; Nadia studying |
| Your Bedroom | Study (1 hour, 5 energy) | none |
| Faculty Offices | none alone | See your advisor (Walsh, office hours, after P16) |
| Cafeteria | Buy lunch ($4, 20 min, +15 energy) | Rosa at the counter |
| The Quad | Sit on the grass (30 min, +5 energy) | Zoe (P20), Jake (P25) |
| Café | Work an hour or a shift (any hour Tom or Chris is in) | Tom; Chris behind the counter |

### 8g. Reputation and talk

Goal 2 reads it: her name on campus opens the party she hosts. One meter, Reputation (campus),
0–100, words: Nobody · Noticed · Talked about · Known · Everyone's talking. Starts at 0. Shown,
still, in release 1. What people say grows with what she wears and does (release 2 on).

Talk at home is separate: what the neighbours and Frank pass to Laura and Mark. Flags, release 2.

| place | alone | with a person |
|---|---|---|
| Women's Bathroom (campus) | Listen to the girls at the mirror (10 min): one overheard line | the girls; Brooke |
| Cafeteria | Listen to the next table (during lunch): one overheard line | the lunch crowd |
| Her street | none | the neighbours' one noticing line |

The overheard lines in release 1 are about other people (Brooke, the party, Hale), true at
Reputation 0: nobody is talking about her yet.

Who throws the parties (LO 2026-11-21: "yes zoe can throw the party"): Zoe, at her apartment,
from release 3. How Reputation and the party connect (proposed, waiting for LO's answer):
| Reputation | at Zoe's party |
|---|---|
| Nobody (0–19) | she goes as Zoe's friend; nobody knows her name |
| Noticed (20–39) | people come and talk to her; Jake's friends look |
| Talked about (40–59) | she's invited by name, not just as Zoe's friend; Brooke starts watching |
| Known (60–79) | Zoe asks her to co-host |
| Everyone's talking (80–100) | she throws her own; that night ends goal 2 |
What raises it: being seen at the party, what she wears there, what she does (a kiss, a dare).
What lowers it: Brooke's talk. The party feeds Reputation; Reputation opens the bigger party.

Beyond parties (LO 2026-11-21: "add more stuffs like prom, and prom queen ... does it only affects
in parties prom or in college too??"). Proposed, waiting for LO's answer:
- No formal (LO 2026-11-21: "remove formal from the idea. We will have parties."). Parties carry
  goal 2: Zoe's, then her own.
- Reputation also reads, on campus: who sits with her at lunch (cafeteria); the drama lead (Cross
  casts it, Brooke wants it); the regulars who come to the café for her (tips, release 3); invites
  by name to Zoe's parties; what Hale and Pratt say in class; Brooke's report to the dean.

### 8h. Nights out

Release 1 (LO 2026-11-21: "basic would be zoe giving very basic dare, and player doesnt accept it",
"no pool"): a basic party at Zoe's apartment, Saturdays 9pm to 1am, once she has met Zoe (P20).
Music, a drink in her hand, a full room; Brooke and her two friends there; one overheard line.
Zoe gives one very basic dare, the same every time: "Go dance with the guy by the speaker." Her
answer is no: "Not tonight." Zoe: "Next time, then. I'm holding you to it." She goes home. Time and
energy only; nothing moves. Later: a "Do it" button beside the no, once meters climb (release 2 or 3).

| place | alone | with a person |
|---|---|---|
| Zoe's Apartment | Go to Zoe's party (Saturdays, 9pm to 1am) | Zoe's dare; Sam; Brooke and her friends |

Area 7 settled (LO 2026-11-21): Brooke is the queen of campus parties, with two friends (Kayla Moore,
20, loud, laughs at everything Brooke says; Tess Harper, 21, quiet and meaner; LO "yes names"); the three bully Ella.
The Sunday ranking board on the quad: Brooke on top, Ella not on it; release 1, it never changes.
Ella's own party is not in release 1; where it happens is decided in its release.

### 8i. What the goals read

Goal 1 reads one counter: Sundays paid in full in a row, 0 to 4, on goal 1's card ("Paid in full:
2 of 4 Sundays"). A short Sunday sets it to 0; at 4, `pays_her_own_way` and the card says "Done.
You pay your own way." with goal 2 named as next, in a later release. It counts in release 1 (LO
2026-11-21: "yes count the sundays"). Goal 2 reads Reputation (8g). Goal 3: later.

## 9. Schedules

### 9a. Home (LO "yes", 2026-11-21)

Jobs: Laura, dental receptionist, weekdays 8:30–5. Mark, warehouse foreman, weekdays 7:30–4:30;
Saturday nights at the bar (not shown in release 1). Ryan dropped out of college; car repair shop,
weekdays 12–6.

Weekdays:
| time | Laura | Mark | Ryan |
|---|---|---|---|
| 7–8 | Kitchen (breakfast) | Kitchen, leaves 7:30 | his room 7–7:12, the hall 7:12–7:25 waiting for the bathroom, Bathroom 7:25–7:45 (LO "yes" 2026-11-21; the hall row LO "Yes" 2026-11-23), then his room |
| 8–12 | at work | at work | his room |
| 12–5 | at work | at work, home 4:30 | at the repair shop |
| 5–7 | Kitchen (dinner) | Living Room (his chair) | home 6, Kitchen |
| 7–11 | Living Room | Living Room | Living Room (the couch) |
| 11–7 | Master Bedroom | Master Bedroom | his room |

Weekends:
| time | Laura | Mark | Ryan |
|---|---|---|---|
| 8–10 | Kitchen | Kitchen | asleep, his room |
| 10–12 | Kitchen | Sunday: Kitchen table (rent) · Saturday: Living Room | Bathroom, then his room |
| 12–5 | out (shopping, friends) | Living Room | Living Room |
| 5–7 | Kitchen (dinner) | Living Room | Kitchen |
| 7–11 | Living Room | Saturday: out at the bar · Sunday: Living Room | his room or the couch |

Reach at home, rough: Laura ~55 h a week, Mark ~50, Ryan ~50 (C159 floor 18). Ryan alone in the
house: weekday mornings 8–12 (Friday has no lectures).

### 9b. Campus (LO "yes", 2026-11-21)

| person | where and when | reach, rough h/week |
|---|---|---|
| Dr. Hale | Lecture Hall Mon/Wed 9–11 · his office Mon/Wed 2–5 (office hours) | 10 |
| Mr. Pratt | Lecture Hall Mon/Wed 11–1 · his office Mon/Wed 1–3 | 8 |
| Prof. Walsh | Lecture Hall Tue/Thu 9–11 · her office Tue/Thu 2–4 (advisor hours) | 8 |
| Mr. Cross | Theatre Tue/Thu 11–1 (class) · Theatre Tue/Thu/Fri 2–6 (rehearsals) | 16 |
| Nadia | Lecture Hall Mon/Wed 9–11 · Cafeteria Mon/Wed 1–2 · Library weekdays 2–6 | 26 |
| Ms. Ivy Holt | Library desk weekdays 8–4, Saturday 10–4 | 46 |
| Rosa Diaz | Cafeteria counter weekdays 8–4 | 40 |
| Dean Sterling | faculty corridor weekdays 8–5, behind his desk (P47, ENI for LO 2026-11-24: release 1 for his first-day scene only) | 0 |

Her café hours (any hour, 8f) clash with classes, office hours, rehearsals and Nadia in the library: money
or people, every weekday afternoon. Hale's later loop (his office after hours) must open 18+ hours a
week (C159), e.g. Mon–Thu 5–8.

### 9c. Neighbourhood and café (LO "yes", 2026-11-21)

| person | where and when | reach, rough h/week |
|---|---|---|
| Mr. Vance | his porch, weekdays 5–8pm · weekends 9–12 and 5–8pm | 27 |
| Frank Novak | Corner Shop, Mon–Sat 7am–3pm | 48 |
| Danny Price | Corner Shop, every day 3–11pm, and all day Sunday | 60 |
| Marco Silva | Gym, weekdays 6–10am and 5–9pm, Saturday 8am–2pm | 46 |
| Nina Kovac | Clothes Shop, Mon–Sat 10am–7pm | 54 |
| Tom | Café, Mon–Sat 10am–9pm; Sunday off | 66 |
| Chris Dale | Café, weekdays 7am–3pm, weekends 10am–8pm (to 8pm: he closes up after the last shift; ENI for LO, delegated 2026-11-24) | 60 |

Vance's porch hours are when she comes home. Sunday shifts are Chris alone. Chris hands the counter
over to her at 2pm on weekdays.

### 9d. Zoe, Jake, Brooke, Kayla, Tess, Sam (LO "yes", 2026-11-21)

| person | where and when | rough hours a week she can reach them |
|---|---|---|
| Zoe | Quad, weekdays 1–3 · Cafeteria Tue/Thu 1–2 · her apartment, every evening 6–11 · her party, Saturday 9pm–1am | 40 |
| Jake | Cafeteria, weekdays 12–2 · Quad, weekdays 2–4 | 20 |
| Brooke | Lecture Hall Mon/Wed 9–11 (Hale's class) · Theatre Tue/Thu 11–1 and rehearsals Tue/Thu/Fri 2–6 · Women's Bathroom mirror, weekdays 8–9 and 1–2 · Zoe's party, Saturday | 35 |
| Kayla and Tess | with Brooke: the bathroom mirror, weekdays 8–9 and 1–2 · Cafeteria, weekdays 12–1 · Zoe's party, Saturday | 19 |
| Sam | Zoe's apartment, every day 12pm–2am (he's always home) | 98 |

## 10. What she walks into

### 10a. Home (LO "yes", 2026-11-21)

LO 2026-11-21: "Hearing someone having sex is not hot, prefer peeking or watching." Every sex
walk-in is seen, not heard.

| scene | kind | who | everyday? | window (§9a) | how often | her choice |
|---|---|---|---|---|---|---|
| Their door's open a crack: Laura and Mark in bed, seen from the hall | she walks in on | Laura, Mark | no | weekdays 11pm–1am, the hall | once a night | Watch · Back away |
| His door's open a crack: Ryan, porn on his phone, nothing about her (D1) | she walks in on | Ryan | no | weekdays 11pm–1am, the hall | once a night | Watch · Back away |
| Laura at the kitchen table with the bills, crying quietly | she walks in on | Laura | yes | weekdays 5–6pm, Kitchen | once a day | Sit with her · Say you're late |
| Mark on the phone to Vance: "I'll have it Friday." | she walks in on | Mark | yes | weekdays 4:30–5pm, Living Room | once a day | Listen from the hall · Walk in |
| Ryan on the couch with a controller: "Want a go?" | she walks in on | Ryan | yes | weekends 12–5pm, Living Room | once a day | Play a round · Not now |
| Ryan comes back for his razor while she showers; "Shit, sorry," and he backs out | walks in on her | Ryan | no | weekdays 7:45–8:30 (ENI for LO 2026-11-24, matches Ryan's 7:25–7:45 bathroom row), on Shower, chance 0.25 | once a day | Cover up · Keep washing |

Count: 6 scenes, 3 everyday (half, C802); 6 of 6 name someone she knows (C678). Each housemate has
at least one (C28). Release 1: a flag each, no meter. Ryan shows nothing about her (LO, relayed
2026-11-21; craft/walk-ins.md step 13).

### 10b. Neighbourhood (LO "yes", 2026-11-21)

| scene | kind | who | everyday? | window (§9c, place hours) | how often | her choice |
|---|---|---|---|---|---|---|
| The park couple: a man and a woman on the grass behind the pond, seen through the bushes | she walks in on | strangers | no | every day 7–9pm, Park | once a day | Watch · Back away |
| Vance on his porch with a ledger of envelopes, licking his thumb, counting | she walks in on | Vance | yes | weekdays 5–8pm, her street | once a day | Say hello · Walk past |
| Danny selling something small out the shop's back door | she walks in on | Danny | yes | every day 9–11pm, Corner Shop | once a day | Pretend you didn't see · Ask what that was |
| Marco "fixing" a woman's squat, hands on her hips longer than he needs | she walks in on | Marco | no | weekdays 5–9pm, Gym | once a day | Watch from the bench · Back to your workout |
| Nina in the fitting room in the shop's tightest dress: "Don't tell my boss. I'm the boss." | she walks in on | Nina | yes | Mon–Sat 6:45–7pm (ENI for LO 2026-11-24, after the try-on closes at 18:45), Clothes Shop | once a day | Tell her it suits her · Just browse |
| A man yanks the fitting-room curtain while she's half in a dress; "Oh, Christ, sorry," and he drops it | walks in on her | a stranger | no | on Try it on, chance 0.25 | once a day | Pull it shut · Finish changing |

Count: 6 scenes, 3 everyday (C802); 4 of 6 name someone she knows (C678). Seen, not heard. Release
1: a flag each, no meter. Vance is "the man next door" in these until P24 names him.

### 10c. Campus (LO "yes", 2026-11-21)

| scene | kind | who | everyday? | window (§9b, §9d, place hours) | how often | her choice |
|---|---|---|---|---|---|---|
| The library back stacks: a couple against the shelves, seen through the gap in the books | she walks in on | strangers | no | every day 6–10pm, Library | once a day | Watch · Back away |
| Hale's door ajar in office hours: he's alone with a file, a yellow note on it, "Nadia — spring" | she walks in on | Hale | yes | Mon/Wed 2–5pm, Faculty Offices | once a day | Knock · Walk on |
| Ms. Holt at the desk, a romance novel inside a library-science cover | she walks in on | Ivy Holt | yes | weekdays 8am–4pm, Library | once a day | Ask what she's reading · Leave her to it |
| Tess doing Brooke's make-up at the mirror, Kayla holding the bag, all three on one guy's name | she walks in on | Brooke, Kayla, Tess | yes | weekdays 8–9am and 1–2pm, Women's Bathroom | once a day | Fix your hair beside them · Leave |
| Cross running a scene with Brooke: "Again. Slower." His hand on her waist | she walks in on | Cross, Brooke | no | Tue/Thu/Fri 2–6pm, Theatre | once a day | Watch from the back row · Leave |
| Cross in the dark seats while she practises alone; one clap: "Again. Louder." | walks in on her | Cross | yes | on Practise on the stage, Tue/Thu/Fri 2–6pm, chance 0.25 | once a day | Do it again · Get off the stage |

Count: 6 scenes, 4 everyday (early share 65%, C802); 5 of 6 name someone she knows (C678). Seen,
not heard. Release 1: a flag each, no meter. People not met yet show as "a professor", "the
librarian", "three girls" until their meeting pieces.

### 10d. Near campus (LO "yes", 2026-11-21)

| scene | kind | who | everyday? | window (§9c, §9d) | how often | her choice |
|---|---|---|---|---|---|---|
| Zoe and Sam on the sofa, Zoe on top, seen from the hall door | she walks in on | Zoe, Sam | no | every day 6–11pm, Zoe's Apartment | once a day | Watch · Back out the door |
| Sam alone on the sofa with a guitar he can't play: "Be honest. Was that a song?" | she walks in on | Sam | yes | afternoons 12–6pm, after P27 | once a day | Tell him the truth · Lie |
| Zoe at the mirror with three outfits on the bed: "Which one says I don't care?" | she walks in on | Zoe | yes | every day 6–9pm, Zoe's Apartment | once a day | Pick one · Tell her the one she's wearing |
| Tom counting the tip jar after close, folding two bills into his own pocket | she walks in on | Tom | yes | Mon–Sat 8–9pm, Café | once a day | Say nothing · "Those are tips." |
| Chris in the storeroom with a regular, her skirt up, his hand under it | she walks in on | Chris | no | weekends 10am–7pm, Café | once a day | Watch from the door · Back out |
| A couple in Zoe's bathroom at the party, door unlocked | she walks in on | strangers | no | Saturdays 9pm–1am, at the party | once a party | Watch · Shut the door |

Count: 6 scenes, 3 everyday (C802); 5 of 6 name someone she knows (C678). Seen, not heard. Release
1: a flag each, no meter. Zoe's apartment needs zoe_place_known (P20).

