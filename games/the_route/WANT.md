# The Want — THE ROUTE

> Doctrine and the reasoning behind each field: `.claude/skills/author-game-v2/references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.

---

## 1. Who the player is — answered BEFORE she is described

**Who is the player?** `female`. Chosen, not inherited: 49 corpus comments ask for a female lead
against 11 opposed, and the opposed get argued down in their own threads.

**Written character, or blank slate?** `written`. Also chosen, and this is the first v2 game to
write the choice down. The field runs 19 blank to 10 written and blank carries 80.4% of the
engagement — so the freedom that buys is bought here two other ways instead, below.

**What does the player choose about her at minute zero?**

**A memory, not a slider.** The intake scene on her first shift is already asking it, so it asks it
out loud: *what were you doing before you came back?* Three answers, and each one buys **reach**,
not flavour.

| flag | what she was | what it opens |
|---|---|---|
| `past_hospital` | four years a floor nurse in the city | the **clinical** rungs — wound care, the injection, the line. Inside bodies the other aides are not allowed to touch. |
| `past_bar` | six years waiting tables and tending bar | the **handling** rungs — talk him down, take the hand off, come back after. The after-hours end of the route. |
| `past_home` | never left; nursed her mother at home for two years | **standing keys.** She has the door codes already, so the night reach on Roy's house opens earlier than it can for anyone else. |

Read at five sites each — a three-band ladder on each of the three daily work surfaces, plus a
paired privilege rung on each. **Additive only:** every original rung keeps its numbers and gains
`<flag> is_false`, so no door closes and a save made before a flag existed reads what it read
yesterday. ⚠️ Adjacent `[group]` blocks merge into one if/elseif chain (`v2.py:14637`), so the past
ladder is separated from a surface's existing ladder by a non-`group` block or the existing one goes
dark with no error.

**The second freedom: the player names two of them.** `npcs[].relationship_options` renders a
picker on the creation screen and the prose reads it back as `@<npc>.rel`. It is written eleven
times in this whole repo, and it is the move the field actually makes.

- `npc_dane` — `brother` · `half-brother` · `stepbrother` · `cousin`
- `npc_marlon` — `neighbor` · `mom's ex` · `stepfather` · `family friend`

Roy and Ward stay fixed blood: the spine of the charge does not wobble. Three customization fields
total — her name, and those two relations. ⚠️ `customizable = true` also renders a **name textbox**
on that character (`v2.py:9296`), so every line about either man uses `@dane` / `@marlon` and never
a typed name.

## 1b. Who she is

**Nora Ashby, 27.** Licensed home health aide for the county agency out of Rossiter. Six houses on
a fixed route off County Road 9, and two of them are her own family.

Her father **Roy** had a stroke eight months ago and his right side never came back. Her uncle
**Ward** holds the power of attorney, which means Ward signs her hours — **she is paid by her
father's brother to put her hands on her father.** Her apartment is over the laundromat in town.
Rent is due weekly and the agency pays weekly, so the two numbers are always in the same week.

**What she has to lose:** the license and the route. Both are revocable by one woman, and the route
is the only thing that puts her inside any of those doors. Off the route she is a relative who has
to knock.

## 2. The appetite that never fills

**To be wanted by men who cannot get through a day without her hands on them.**

It cannot complete. Need resets every morning — that is what a body is — and every man who starts
needing her a notch more than the sheet says pulls it further in. There is no amount of being needed
that settles it, because the thing she wants is the moment the needing stops being clinical, and
that moment has to happen again tomorrow.

**What does release 41 add?** A new house on the route, a new hour of the day, or a relative who
moves into one of the houses already on it. The county keeps assigning and the family keeps
collapsing back toward each other; neither runs out.

## 3. What she is becoming — as ACCESS

**Bottom:** an assigned route. Two hours a house, daylight only, gloves on, a checklist Cheryl reads
back to her on Friday. She knocks, she waits, she leaves when the sheet says leave.

**Top:** keys to four houses, her own hours, night visits nobody scheduled, and the checklist a
formality — because by then none of them are calling the agency. They are calling her.

### The ascent tiers — they live on the CAST

`who_climbs = "cast"`, `ascent_tiers = []`. **One willingness word for the whole game — `want` — and
everybody who climbs is on it, on the same scale.** People are told apart by what *modifies* that
number, never by giving them separate vocabularies. Measured over thirteen corpus games: median one
meter per person, nine of thirteen use the same word for everyone, 88% of threshold values shared by
two or more people.

The rich second meter, `access` — what he lets her into — goes to **Roy and Dane only**, the two arcs
that carry the game. Gold-plating the whole cast dilutes the core and triples the authoring.

| character | what `want` means on him | `access` | rungs |
|---|---|---|---|
| `npc_roy` | lets her · asks her to · asks for more than the sheet says · stops pretending it was the sheet · says what he wants while she works | the bathroom door open · the bath chair · his room at night · the key on the hook is hers | ~5, low and uneven |
| `npc_dane` | jokes · stops joking · takes her hand off and puts it back · does not let go · does not wait for the visit | the door unlocked · the bedroom · sits up for it · the trailer is hers whenever | ~5 |
| `npc_ward` | says nothing · says one thing · says it in the kitchen with Roy down the hall · says it to her · stops asking | — | ~3 |
| `npc_marlon` | is careful · is not · says what the relation is out loud · uses it · uses it in front of somebody | — | ~3 |
| `npc_cheryl` | — she is workplace, and willingness does not apply | **`trust`**, and it is the meter that opens the world | ~4 |

**Cheryl's `trust` is the route.** Which houses she is assigned, which hours, whether a night visit
is approved, whose keys she is trusted with. There is **no player ascent tier** — the meter that
widens the map is owned by the one person the Want already says can take the route away, which is
better fiction than a bar on the sidebar and it puts the whole climb on the cast where the
declaration says it lives.

**Rungs are chosen, not copied.** Per-character willingness in the field runs a **median of 3 rungs
(p25 2, p75 6) with the lowest at about 5** — the 8–17 figure belongs to a player ascent meter and
does not transfer. **No ladder starts at 15**, and the reason is `templates/board.toml`, not any game.

## 4. The charge

- [x] **Reversal** — the men whose authority over her was total now need her hands to get through a
      day, and the county pays her by the hour to give them. It flips one man at a time, and each
      flip is a man asking for something the sheet does not list.
- [x] **Taboo** — it is blood, and it is her job, and each fact is the other one's cover. Every
      touch in this game has a clinical name for it, which is exactly what makes it deniable, which
      is exactly what lets it go further.
- [ ] Transformation

## 5. The world

**Where does this happen?** Rossiter — a county seat with an agency office, a gas station, a
laundromat, a diner — and the farm road out of it, where the houses on the route are.

**What is outside the door she wakes up behind?** **County Road 9.** It is the ground the whole game
sits on and it is the title. Every house hangs off it, and it is a **root**, not a hallway off
somebody's kitchen.

**How far can she get from it, and what stops her?** As far as the truck and what is in the tank.
Fuel is a real need, not a flavour, so distance costs money and money is checked before she goes.

**Which shape is this?** — `board.map.archetype`:

- [x] `nested_zones` — the road and the town are the ground; the houses, her apartment and the
      agency office hang off them, and each house opens into its own rooms.
- [ ] `two_hub` · [ ] `map_hotspots` · [ ] `street_mesh` · [ ] `time_slot`

**What does her body need here, and what stops when it goes unmet?**

- **`sleep`** — falls across the day, faster on a double. Filled in her own bed. **Shuts:** low, she
  cannot take the night visits, and the night visits are where the route stops being a job.
- **`hunger`** — falls with hours worked. Filled at the diner, at Roy's kitchen, at home. **Shuts:**
  low, her hands shake and every clinical rung refuses — including the ones `past_hospital` bought.
- **`clean`** — this is body work and it goes both ways. Filled at her apartment, or at a sink in
  whichever house she is standing in. **Shuts:** low, the high rungs on every man refuse.
- **`fuel`** — falls per visit. Filled at the gas station, and it costs. **Shuts:** empty, every
  location past walking distance is closed. This is the one object that wires the economy to the
  map: money does not just price things here, it decides which houses exist today.

**How alive?** Living world, deliberately. The route means traffic she did not summon — the agency
reassigns, the men have hours, a house is dark when she gets there.

## 6. Why *this* person

| character | why they are wanted |
|---|---|
| `npc_roy` | Roy Ashby, 57. Her father. Right side gone since March. He ran everything and decided everything, and now the first hour of his day is her hands on him. Being wanted by him means it was never actually about authority. |
| `npc_dane` | Dane, 29. Home on a rebuilt knee, wife gone, nothing to do all day but wait for the visit. He never had power over her, so his wanting is not a reversal — it is the only appetite in the game with nothing to lose, which makes it the fastest ladder and the least deniable. |
| `npc_ward` | Ward Ashby, 49. Roy's younger brother, holds the power of attorney. He signs the hours, so every dollar she has passed through the hand of the man who decides how long she is alone in that house. He has never once said what he thinks that is worth. |
| `npc_marlon` | Marlon Teague, 44. Six weeks out of back surgery, and whatever the player made him. He is the man on the route who shows her what this is when it is only a job — or, if she named him closer, the one who proves it never was. |
| `npc_cheryl` | Cheryl Pike, 50s. Her supervisor at the agency. The standard, and the brake. She is the only person who knows what the job is supposed to be, and the only one who can take the route away. |

## 7. Register

- **`narration_person`** = `second` — declared once, **immutable** after the first release ships.
- **Locale: plain American, locked here rather than at the gate.** Field games use locale-locked
  nouns at 0.8 per 10,000 words; v2 games run 9.4 to 95.6, inherited from this skill's own worked
  examples. Banned in prose **and on buttons**, where a label cannot carry its own gloss: *flat ·
  chip shop · chemist · jumper · tea (the meal) · meter (the coin box) · pitch (rent) · torch ·
  biscuit · half seven · lodger · forecourt · anorak · bedsit · wellies.* A place is named for what
  it is in the first sentence that names it.
- **What the vocabulary check returned, run on this page:** 44 rare words over 1,887, and almost all
  of them are this file talking to itself — plus six false friends and one ambiguous `half <hour>`
  which are *the ban list above being read as usage*. Do not "fix" those. Two hits are real, because
  both reach the player: **`aide`** is fine in *home health aide*, which glosses itself, but a button
  never says a bare "aide" — it says what she is doing. And **`attorney`** never appears in prose at
  all: Ward **signs the hours**, which is the mechanism; *power of attorney* is the legal name for it
  and the player does not need to hold it.

- **Crude-vocabulary ceiling** — the actual words, per character, per tier. This is a **ceiling and
  never a floor**: writing under it is a defect.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_roy` | none — the shape of her, how close she has to stand, how long it takes | tits, cock, hard — flat, once, said like a symptom | full — cunt, cum, and he stops calling any of it by its clinical name |
| `npc_dane` | tits, ass — he says it on day one and always has | cock, cunt, wet | full, out loud, and he uses whatever relation the player picked while he does |
| `npc_ward` | none aloud; crude in narration only | tits, ass, cock | full, and in the kitchen with Roy down the hall |
| `npc_marlon` | none — he is careful, he is a client | tits, cunt, hard | full, and the ceiling rises with how close the player named him |
| `npc_cheryl` | none | none | none — she is the standard, and the register is what she is the standard against |

- **Where the crude register lives:** the **bath chair** in Roy's bathroom · the **bed change** in
  Dane's trailer · the **dressing** at Marlon's · the **sink** she washes at in whichever house she
  is standing in. Every one of them is entered every in-game day from 0.1. Not one of them is a
  one-time scene, and nothing crude is saved for a room with no exits.

---

## The four checks

1. **What does release 41 add?** A new house on the route, a new hour, or a relative who moves into
   a house already on it. The county renews the cast and the family renews it faster.
2. **What can she reach at the top that she cannot at the bottom?** Four sets of keys, her own
   hours, the houses after dark, and rooms nobody wrote on a sheet — with the checklist reduced to
   something she fills in afterward.
3. **Which character would a player miss if deleted, and why?** **Cheryl.** Roy is the charge and
   Dane is the appetite, but Cheryl is the only person who knows what the job is supposed to be.
   Cut her and nothing Nora does is measured by anyone who understands it, and the route stops being
   something that can be lost.
4. **Which repeatable surface carries the crudest writing in the game?** The **bath chair** in Roy's
   bathroom. It is the first hour of the first house every single day, it is the reversal in one
   object, and there is no version of this route that goes around it.
