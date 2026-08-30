# The Want — Commuter

> Re-read this before every release. Bump `want.last_read_at_release` in `v2_state.json`.
> Doctrine: `.claude/skills/author-game-v2/references/the-want.md`.

---

## 1. Who the player is — answered BEFORE she is described

**Who is the player?** `female`

**Written character, or blank slate?** `written` — chosen, not defaulted. The cast is named and the
media is real-performer, which is what `written` is for. The freedom the field actually pays for is
bought back two other ways below: the start choice, and the relationship picker.

**What does the player choose about her at minute zero?**

A memory, not a slider. First morning of the semester, kitchen table, Gail says something about last
summer. Three answers, one flag each:

| flag | what she did | what it buys |
|---|---|---|
| `past_worked` | worked the whole summer, forty hours, saved none of it | the campus-shift rungs, and Vic already knows her face |
| `past_away` | was gone — a friend's place two states over, back in August | the `seen` rungs early; nobody in the house has looked at her in three months |
| `past_home` | never left the house | the household rungs early; Ray and Cole are used to her being there at 2pm |

Five read sites each. **Additive only** — every original rung keeps its numbers and gains
`<flag> is_false`, so the pair is mutually exclusive and no save loses a line.

⚠️ **Placement:** adjacent `[group]` blocks merge into one if/elseif chain and first match wins
(`v2.py:14637`). Separate the past-ladder from any surface's existing ladder with a non-`group`
block, or that ladder goes dark for every player carrying a past.

**Customization — three fields, plus the picker.** Name (text), plus two free-text fields. The
distinctive axis is the cast, not her: `npcs[].relationship_options` renders a picker on the same
screen and the pick lands on the NPC, read in prose as `@<npc>.rel`.

| character | options (first is the default) |
|---|---|
| `npc_ray` | **stepfather** · mom's husband · father · uncle |
| `npc_cole` | **stepbrother** · half-brother · brother · cousin |

⚠️ `customizable = true` on an NPC also renders a name textbox, so **every line of prose for Ray and
Cole uses `@ray` / `@cole`, never a typed name.**

## 1b. Who she is

**Dana Reed, 19.** Second year at Dutton State, three quarters of a mile from the house she was
twelve in. She rides in because the money went to the payment plan instead of a dorm — the plan is
in her name, the gap is not, and the difference is made up at the kitchen table every week by
a man whose name she does not have. She is the only Reed in the house. One bathroom. Her door has a
lock and she still uses it.

**What she has to lose:** her spot. The house is the only reason she can afford to be a student at
all, and both facts are held by the same two people.

## 2. The appetite that never fills

To be wanted by the men who are supposed to be looking after her, and by the ones who only see her
three hours a week.

It cannot complete. Every degree closer resets the distance — the thing she wanted last month is
just where she stands now, and there is always a next person who has not looked yet.

**What does release 41 add?** A new body in one of the two hubs — a cousin for the summer, a new TA,
somebody's friend who stops leaving — plus the next rung on somebody already standing. Zero new
locations required.

## 3. What she is becoming — as ACCESS

**Bottom:** She dresses in the bathroom and keeps her door shut. On campus she is one of ninety in an
8am section, the buildings lock at nine, and she takes the last bus home.

**Top:** Doors in the house stay open, hers included, and nobody knocks. On campus she has a reason to
be inside a locked building after nine, and she does not always take the last bus.

### The ascent tiers

⚠️ **Rungs are set in the board phase and they do NOT go 15 / 35 / 55 / 75.** All sixteen tiers
across five v2 games put their lowest rung at exactly 15 because `templates/board.toml` had that
table sitting in the slot; the field runs 8–17 rungs starting near 5. This game gets more rungs,
starting lower.

| tier key | going further means | low | mid | high | top |
|---|---|---|---|---|---|
| `house` | how much of the house is hers to be seen in | changes with the door open; comes out of the bathroom without covering up | the hall in a towel; sits in the kitchen in what she slept in | into their rooms without knocking; nobody knocks on hers | nothing in the house is private, and the back bedroom is somewhere she can walk into at night |
| `standing` | what the college lets her be near, and who is asking whom | asks a question after class; gets her name learned | office hours alone with the door shut; a key to the lab cabinet | inside a locked building after nine because somebody let her in; stops taking the last bus | she is the one being asked — for the shift, the favor, the office at six |
| `seen` | who gets to look, and how long she lets them | does not cover up; does not change what she was already wearing | goes out dressed for it; lets a look land and does not break it | lets it be noticed by somebody who will say something out loud | does it where she will be caught, and the catching is the point |

**Counterweight:** none declared. If one is added it is logged as a decision with what it spends.

**The one milestone named here, because the map owes it a room.** At the top of `house`, with Gail's
own relation at its band, a one-time scene turns the **back bedroom** — Ray and Gail's — into a
**standing, repeatable** surface with both of them in it. A milestone that opens nothing is a dead
end; this one names what it opens, and that location must exist in the board.

## 4. The charge

- [x] **Taboo (primary)** — the relationship itself is the transgression, and it lives in a house
      with one bathroom and four people who see each other every morning. The picker lets the player
      set the exact degree; the game is written so every setting of it lands.
- [x] **Transformation (secondary)** — she starts as the kid in that house and ends as the reason
      the other three arrange their evenings.
- [ ] Reversal — available on Ray (he holds the money) but not the spine.

## 5. The world

**Where does this happen?** Dutton — a college town. **Main Street** is the ground: the strip running
from the campus gate down to the houses. Everything else hangs off it.

**What is outside the door she wakes up behind?** The street, immediately. Two strong hubs sit on it
and neither contains the other:

- **Dutton State** — the anchor. Lecture hall, the department building, Doyle's office, the lab, the
  desk she works, the loading door that is unlocked after nine. **This carries the largest single
  block of prose in the game.**
- **the house** — her room, the hall, the one bathroom, Cole's room, the kitchen, the garage, and the
  back bedroom the milestone opens.
- **the tail** — the bus stop, the laundry, a place to eat, the payments window.

⚠️ **The anchor is the campus, not the house.** Eight of nine v2 games rooted the world on one
worksite or one household; the measured reference puts ~30% of all location prose in a school. The
house is the second hub, and it is budgeted like one.

**How far can she get, and what stops her?** The bus, and the clock. Class times are fixed, the shift
is fixed, the buildings lock at nine, and the last bus is the wall — until `standing` moves it.

**Which shape is this?** `nested_zones`. Main Street is a **root**, never a leaf off the kitchen.

**What does her body need here, and what shuts when it goes unmet?**

| need | falls | fills | shuts |
|---|---|---|---|
| `sleep` | overnight and across a long day | her bed; the couch; the lab at 3am | under the band she cannot take the 8am section — the day starts at noon and half the campus rungs are gone |
| `hunger` | across the day | the kitchen; the place on Main | under the band she cannot work a shift or a lab |
| `hygiene` | daily, faster after work | the one bathroom — and it is occupied | under the band she will not go out in public at all |
| `prep` | every day she does not do the reading | her room; the library hour; the lab bench | under the band the classroom rungs are closed, and the only way through is asking Doyle for an extension — which costs a favor |

`prep` is the one the premise adds, and it is the one that feeds the taboo economy directly: the
cheapest way out of it is owing somebody.

**How alive?** Living world. Two hubs with fixed hours means ambient traffic she did not trigger is
cheap — a hall between classes, a kitchen at 6pm, a bus with people already on it.

**No phone.** Refused deliberately (`the-phone.md` P1). The premise's whole friction is that she has
to be physically in a room; a phone dissolves it.

## 6. Why *this* person

| character | why they are wanted |
|---|---|
| `npc_ray` (52) | He pays for the thing that lets her be enrolled, and he has never once acted like it buys him anything — which is exactly why she keeps testing whether it does. |
| `npc_gail` (45) | The only person in the house who was ever looked at the way Dana is starting to be, and she is watching it happen with something that is not entirely warning. Further in she is not the clock — she is in the room. |
| `npc_cole` (22) | Six years sharing a wall and he was never her brother. He is the only one who treats her like she is not a kid, because he never knew her as one. |
| `npc_doyle` (46) | Three hours a week of a man who has to notice her by contract and spends all three pretending he does not. |
| `npc_trevor` (20) | No power over her whatsoever, which is why he is the only one who says it out loud. |
| `npc_vic` (58) | He decides which doors are locked at nine. He has already decided about hers. |

## 7. Register

- **`narration_person`** = `second`. Declared once, **immutable** after the first release.
- **Crude-vocabulary ceiling** — the actual words, per character, per tier. A ceiling is a **ceiling,
  never a floor**; writing under it is a defect.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_ray` | tits, ass, hard | cock, cunt, wet, fuck | cock, cunt, cum, throat, hole, fuck her — and what her body does back |
| `npc_gail` | tits, ass | cunt, wet, fingers, mouth | cunt, cum, tongue, fuck — plus the three-way vocabulary the milestone opens: between them, both of them, her turn |
| `npc_cole` | tits, ass, hard, cock | cunt, wet, fuck, cum | the coarsest register in the game — nothing withheld, because he has nothing to protect |
| `npc_doyle` | withheld and clinical: her mouth, her knees, the desk | cock, cunt, wet | fuck, cunt, cum, on her knees in an office — crude, but still in his voice |
| `npc_trevor` | tits, hard, cock | cunt, fuck, cum | crude and unembarrassed; he has never had a reason to be careful |
| `npc_vic` | ass, tits | cock, cunt | fuck, cum, cunt, throat |

- **Where the crude register lives:** the **repeatable** surfaces, and this is the correction the
  whole skill exists for. Named: the hall and the one bathroom · Cole's room · the kitchen on the
  nights Gail is on shift · Doyle's office after six · the lab at close · the loading door after nine
  · the last bus · and the back bedroom once the milestone opens it.

  **Not** a capstone. If the crudest writing in this game ends up in a scene the player sees once,
  the game is cold and the release does not ship.

## Economy

| | |
|---|---|
| currency / symbol | money · `$` |
| **obligation** | the school payment — weekly, in person, at the payments window |
| `obligation_amount` | 180 |
| `week_income` | 260 — the campus shift, plus asking at the kitchen table, plus the odd cash hour |
| sinks | the school payment · the bus pass · food · laundry · clothes that feed `seen` |

⚠️ **The obligation is not rent.** Nine of nine v2 games ran a rent-or-debt hook. This one is a
payment plan in her own name, and the gap is the lever: the difference between 180 and what a week of
shifts actually pays is what she has to ask for, and asking has a price at that table.

---

## The four checks

1. **What does release 41 add?** A new body in a hub that already exists, and the next rung on
   somebody already standing. Zero new locations. ✅
2. **What can she reach at the top that she cannot at the bottom?** Her own hall in a towel; rooms
   she does not knock on; a locked campus building after nine; the back bedroom, with both of them
   in it. ✅
3. **Which character would a player miss if deleted?** Gail. She is the only one who is the obstacle
   and the target and the mirror at once, and the milestone that opens the back bedroom is
   unwritable without her. ✅
4. **Which repeatable surface carries the crudest writing?** Cole's room and the one bathroom, both
   re-enterable from day one. ✅
5. **Vocabulary check** — run and read below.
