# The Want — MRS. VANCE

> Doctrine and the reasoning behind each field: `.claude/skills/author-game-v2/references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.

---

## 1. Who she is

**Rilla Vance, 27**, née Marek. Eleven weeks married to **Dorn Vance, 54**, who owns Vance Diesel —
a repair yard on the county road outside Kerr Crossing, with the house sitting out back on the same
gravel lot. She signed a paper before the wedding: nothing is hers for three years. No car in her
name, not on the account, sixty dollars a week in an envelope on the kitchen counter.

Dorn put her on **the books**. She writes down every number the yard makes and cannot touch one of
them. She hands the week's cash to his eldest son on Friday.

**Dorn hauls four nights out of seven.** So the man whose authority she is borrowing is gone most of
the week, and the four men the paper says she is over are all still here.

**What she has to lose:** the three years. Walk out before then and she leaves with the two bags she
arrived with — and her brother loses the job she got him.

## 2. The appetite that never fills

**To be wanted by men who have to call her by a title she did not earn.**

It cannot complete. There is no figure of respect she can reach that settles it; every man who
starts using her name instead of the title has to be replaced by one still using the title, and the
yard supplies them — drivers, hires, family home from somewhere.

**What does release 41 add?** A new hire in the bunk room, a customer who becomes a regular, or
another Vance who turns up needing a place to sleep.

## 3. What she is becoming — as ACCESS

**Bottom:** the office counter and the front rooms of the house, in daylight, with Dorn's name doing
all the work. She asks Cade for the truck when she wants to leave the property.

**Top:** the shop floor after close, the bunk room over it, the wash bay at midnight, the back row where the overnight trucks park — and none of it needing his name, because by then they are not calling her by it.

### The ascent tiers — they live on the CAST, not on her

`who_climbs = "cast"`. Five men, five ladders, each two meters: **access** — what she is allowed to
be near — and **willingness** — how far he will go. Nothing here is one global corruption bar, and a
player who does not want one man's ladder can climb another. *(Exact engine keys pinned in the board
phase, not here.)*

| character | access — what he lets her into | willingness — how far he goes |
|---|---|---|
| `npc_cade` | signs her in · the drawer key · the shop after close · the bunk room · his truck | makes her stand there while he counts · hands on her at the desk · uses the office · the wash bay · does not stop when headlights come up the road |
| `npc_isaac` | will not look · looks · the bunk room · the loft · sleeps with the door open | watches · wants to be caught at it · is watched back · touches · takes |
| `npc_booth` | says Mrs. Vance · says Rilla · her doorway · her bathroom · her bed | does not know what he wants · knows · asks · takes · stops pretending she is anyone's wife |
| `npc_sherrod` | has not said what he is owed · says it · the stairs over the office · the room · the key | collects small · collects properly · collects in front of the others · collects whenever he likes |
| `npc_tobin` | pretends not to see · sees · the bunk room · alone · the two of them and no one else | says nothing · says it · once · as a habit · the only one using her name while he does it |

**Rungs are chosen, not copied.** Placed low and unevenly — the field runs 8–17 rungs opening near 5.
No ladder starts at 15.

**Counterweight:** `standing` — how much of the Vance name is actually hers. It rises when a man
treats her as his father's wife in front of someone, and falls when he treats her as something else
in front of someone. **It is read constantly and refuses almost nothing** — the bank clerk's tone,
whether a driver at the counter talks to her or asks for a man, what the bar already knows. A colour
meter, not a gate.

## 4. The charge

- [x] **Reversal** — the title is hers and everything under it is theirs: the money, the truck, the
      job her brother has, the room she sleeps in. It flips one man at a time, and each flip is a
      man deciding out loud that the title does not apply to him.
- [x] **Taboo** — carried hardest by **Booth**, who is nineteen and means the title, and by
      **Tobin**, who is her blood and the only person here who knew her before it.
- [ ] Transformation

## 5. The world

**Where does this happen?** Vance Diesel — a repair yard on a county road, twenty minutes out of
Kerr Crossing. Shop, office, bunk room over the shop, wash bay, a back row where trucks park overnight, each with a bed behind the seats, and the house on the same gravel lot.

**What is outside the door she wakes up behind?** The lot, and the road it meets. Both are open
ground and both are the reason this is a world rather than a floor plan: the road brings drivers who
were never here before, and the lot is where anyone can see anything.

**How far can she get from it, and what stops her?** Twenty minutes to Kerr Crossing, and no car in
her name. She takes the shop truck, which means asking Cade — so leaving the property is itself a
read of a cast meter.

**Which shape is this?** — `board.map.archetype`:

- [x] `nested_zones` — the lot and the road are the ground; the house, the shop and the back row
      hang off them, and Kerr Crossing is a second ground reached across a bridge that costs time.
- [ ] `two_hub` · [ ] `map_hotspots` · [ ] `street_mesh` · [ ] `time_slot`

**What does her body need here, and what stops when it goes unmet?**

- **`energy`** — falls across the day, faster on shop work. Filled by sleeping in her room.
  **Shuts:** low, she cannot take the office late, which is when the office is worth being in.
- **`clean`** — falls on shop work and on weather. Filled in the house bathroom, or in the **wash
  bay**, which is not a private room. **Shuts:** low, she will not sit at the family table and will
  not stand at the counter when a customer comes in.

**How alive?** Living world, deliberately. The yard has customers she did not summon, the men have
hours, and the week has a shape because Dorn's truck is in the lot or it is not.

## 6. Why *this* person

| character | why they are wanted |
|---|---|
| `npc_cade` | Cade Vance, 29. Runs the yard, two years older than his stepmother. He never once pretended the marriage was normal, and he is the one who decides what she is allowed to touch. |
| `npc_isaac` | Isaac Vance, 24. Sleeps in the bunk room over the shop. He watches and says nothing, and being watched by him was the first thing about this place she liked. |
| `npc_booth` | Booth Vance, 19. Still in the house. He is the only one who takes the title at face value and means it — and undoing that is the whole taboo. |
| `npc_sherrod` | Sherrod Vance, 51. Dorn's brother, lives over the office. He arranged this, more or less, and has never once said what he thinks he is owed. |
| `npc_tobin` | Tobin Marek, 22. Her brother, and she got him the job. The only person alive who knew her before the title, and the only one who can say out loud what she married into. |
| `npc_dorn` | Dorn Vance, 54. The husband. He is the clock and not a hub: three nights his truck is in the lot and four nights it is not, and the whole week is which. |

## 7. Register

- **`narration_person`** = `second` — declared once, **immutable** after the first release ships.
- **Locale:** American-neutral nouns, locked here rather than at the gate. Already cut from prose and
  buttons: *forecourt*, *apron*, *frontage*, *tyre*, *lorry*.
- **Crude-vocabulary ceiling** — the actual words, per character, per tier. A ceiling described
  abstractly gets written around. This is a **ceiling and never a floor**: writing under it is a
  defect.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_cade` | tits, ass | cock, cunt | full — cum, and he says all of it out loud |
| `npc_isaac` | tits | cunt, cock | full, and mostly in narration — he still barely talks |
| `npc_booth` | none — he cannot make himself say any of it | tits, cock | full, and he is still calling her Mrs. Vance while he does |
| `npc_sherrod` | cunt, tits — he opens here, he never pretended | full | full, and in front of whoever is standing there |
| `npc_tobin` | none | none aloud; crude in narration only | full — and he is the only one using her name |

- **Where the crude register lives:** the **Office after close**, the **Wash Bay**, the **Bunk
  Room**, the **Back Row**, the **Shop Floor**. Every one of them is a surface she re-enters. Not one
  of them is a one-time scene.

---

## The four checks

1. **What does release 41 add?** A new hire in the bunk room, a driver who becomes a regular, or
   another Vance needing a bed. The yard renews its own cast; the road renews it faster.
2. **What can she reach at the top that she cannot at the bottom?** The shop after close, the bunk
   room, the loft, the wash bay at night, the back row where the overnight trucks park, the stairs over the office —
   and the truck without asking.
3. **Which character would a player miss if deleted, and why?** **Booth.** Cade is the ladder with
   the most rungs, but Booth is the only one who believes the title, and the game stops meaning
   anything the moment nobody does.
4. **Which repeatable surface carries the crudest writing in the game?** The **Wash Bay** — it is
   how she fixes `clean`, so she is routed into it by her own body, and it has no door.
