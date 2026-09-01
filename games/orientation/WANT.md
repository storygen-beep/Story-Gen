# The Want — Orientation

> Re-read before every release. Bump `want.last_read_at_release` in `v2_state.json`.
> Doctrine: `.claude/skills/author-game-v2/references/the-want.md`.
> Everyone in this game is eighteen or older. Josie is eighteen and has started college.

---

## 1. Who the player is — answered before she is described

**Who is the player?** `female`. Declared, not defaulted.

**Written character, or blank slate?** **`blank`** — and this is the first v2 game to pick it.
The field runs 19 blank to 10 written and blank carries 80.4% of the top-30's engagement; eight
prior v2 games are `written` and no ledger records anyone choosing it. The premise is the best fit
for blank this repo will get: she is eighteen, it is her first night in the house, and **nobody in
it has a read on her.** Blank here means *we do not write her past* — not that she has no face. The
media is real-performer, so her body is fixed by the clips regardless.

**What does the player choose about her at minute zero?**

A memory, not a slider. On the arrival night Wes asks what she was at her old school — the scene is
already asking it — and the answer sets one flag. No stat screen.

| flag | the memory | what it buys — REACH, not flavour |
|---|---|---|
| `past_top` | she was the one with the grades | Halloran hands her the reader's key in week one; the late lab is reachable before anyone else's |
| `past_crowd` | she ran with people two years older | Simone walks her past the sign-in book; the upstairs is not a stranger |
| `past_nobody` | nobody at her old school knew her name | she is not clocked where she should not be — and reputation climbing from zero is worth more |

**Five read sites each. ADDITIVE ONLY:** every original rung keeps every number it had and gains
`<flag> is_false`, so the pair is mutually exclusive and no door closes.

⚠️ **Placement trap.** Adjacent `[group]` blocks merge into ONE if/elseif chain (`v2.py:14637`) and
first match wins. Separate any past-ladder from a surface's existing ladder with a non-`group`
block, or the original ladder goes dark with no error.

**The creation screen — three fields, and the axis is the cast.**

1. her name (`text`, reserved id `name`)
2. **what Ray is to her** — `relationship_options` on `npc_ray`
3. **what Wes is to her** — `relationship_options` on `npc_wes`

Read back in prose as `@player`, `@ray.rel`, `@wes.rel`. Verified on the default build path:
`game_graph.py:164-165` → `v2.py:911` → `v2.py:9282`.

⚠️ **`v2.py:9294` emits a name textbox for every customizable NPC, unconditionally.** So Ray and Wes
can both be renamed by the player, and **every line of prose about them uses `@ray` / `@wes` and
never a typed name.** Dee, Simone and Halloran stay fixed.

## 1b. Who she is

**Josie Marsh, 18.** Two suitcases in a room that was an office until Sunday. Her mother married
Ray Kessler in June and the house came with him, and with his son Wes, 20, a junior at the college
she starts tomorrow. She has been in this house four hours.

**What she has to lose:** nobody here has a read on her yet. That is the only thing she owns, and
every rung spends some of it.

**What she owes, who collects it, and when:** tuition is Ray's. **Everything college charges on top
of tuition is hers** — dues, the meal plan, the lab kit, the bus. **Friday, at the pledge house,
Simone counts the dues on the office desk** and writes a name down if the number is short.

- opening amount **$120** against an honest week of **~$260** (46%)
- it **moves** by *cost follows holdings* — every commitment she signs adds weekly upkeep. The rise
  is hers, it is legible, and no collector has to justify it.
- **The offer, and it is reachable while she is fine:** Ray covers the dues before she needs it.
  Owing him opens his ladder. It is **not** gated on being short. The money is charged by campus and
  the debt lands at home — that is the ignition and the taboo in one move.

## 2. The appetite — where she lands, not where she starts

**To be the one who gets asked — by the people who set the rules, in the rooms where the rules are
set — and to hear her own name said in a room she has not walked into yet.**

It cannot complete. Every room she gets into has a room behind it, and the campus keeps supplying
people who have not looked at her yet.

**Where the bill stops being the reason:** the Friday she has the dues folded in her pocket, walks
past the office desk, and asks Ray for it anyway.

## 3. What she is becoming — as ACCESS

**Bottom:** the lecture hall, the dining hall, the sign-in book at the pledge house, and the
upstairs bathroom at home when it is free.

**Top:** up the stairs at the house on a party night without being stopped · into Halloran's office
after the department has emptied · into the kitchen at one in the morning when Ray is the only one
awake and nobody is pretending it is about the dues.

### The ascent tiers — `who_climbs = "player"`

| tier | what going further means on this axis | rungs |
|---|---|---|
| `nerve` | doing it where someone can see | 5 · 15 · 30 · 50 · 70 · 90 |
| `appetite` | what she will take, and whether she is the one who asks | 5 · 15 · 30 · 50 · 70 · 90 |
| `reputation` | how much of campus has heard. Rises, almost never refuses, **delivers people** | 10 · 25 · 45 · 65 · 85 |

⚠️ **Rungs start at 5, not 15.** All sixteen declared tiers across five v2 games put their lowest
rung at exactly 15 because `templates/board.toml` carries that table; the field runs 8–17 rungs
starting around 5.

**Counterweight: `home_face`** — what the household still believes about her. Campus raises the
three; carrying it home spends this. **Spending it is what opens Ray.** It is the wire between the
two charges, and it shuts doors: while it is high, Ray will not move.

**What does release 41 add?** `reputation` 85 opens the other house on the row — a corner of campus
that has already heard about her before she walks in, with people who arrive knowing.

## 4. The charge

- **Taboo** — the household. Legally family, four hours old, and the debt is what makes it move.
- **Transformation** — she becomes someone the girl who unpacked two suitcases would not recognise,
  and college is what does it, not the house.

Both, deliberately. **Taboo drives the house track, transformation drives the campus track, and
`home_face` is the wire between them.**

## 5. The world

**Where does this happen?** A college town. Two strong places: the Kessler house on the near side,
and the campus with the row of houses along its east edge.

**What is outside the door she wakes up behind?** The avenue, with the stop on it. The bus is $ and
forty minutes; **a ride from Wes or Ray is a favour** — the bridge is itself a surface.

**How far can she get from it, and what stops her?** Money, the clock, and whether anyone will drive
her.

**Which shape is this?** — **`two_hub`**. Two strong places joined by a commute. Not
`nested_zones`: five v2 games are nested and the doctrine names it the default to beat, and the
premise is honestly two grounds, not one nested one.

- `home_base` — her room in the Kessler house
- `exterior` — **the avenue**, a ROOT, not a leaf off the kitchen
- **anchor** (~30% of the world's prose) — **the pledge house**, on campus. Not the kitchen.

**What does her body need here, and what does each one SHUT?**

| need | falls | fills | shuts |
|---|---|---|---|
| `rest` | daily | her bed, the house | under 30 the eight o'clock is closed — and Halloran's rungs run through attendance |
| `clean` | daily | the shared bathroom at home, the house's upstairs bath on campus | under 40 she will not go where she is looked at — every `nerve` rung is shut |
| `fed` | daily | the dining hall (meal plan), the house kitchen | ⚠️ **on probation.** Cut it at board unless it earns a real shut. |

**How alive?** Living world. Ambient traffic on campus and routines in the house she did not
trigger — the two hubs have to feel like they run without her, or arriving means nothing.

## 6. Why *this* person

| character | why they are wanted |
|---|---|
| `npc_ray` | the first adult who looks at her like the room changed when she walked in — and the one person she cannot afford to lose, because he is the reason she is enrolled at all |
| `npc_wes` | he was already inside every room she is trying to get into, and he is the only person who sees both halves of her life |
| `npc_dee` | not wanted — **she is the price tag.** Every hour Ray is alone with her is an hour Dee is on shift, and that is what makes it cost |
| `npc_simone` | she decides who Josie gets to be on that campus, and she says so out loud. Being chosen by her is the fantasy; being billed by her is the engine |
| `npc_halloran` | the one man whose approval is worth something on paper — and the only one who can hand her a key |

## 7. Register

- **`narration_person` = `second`** — declared once, **immutable** after the first release.
- **Crude-vocabulary ceiling** — the actual words, per character, per tier. A ceiling described
  abstractly gets written around. This is a ceiling, never a floor; writing under it is a defect.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_ray` | tits · ass · hard · his cock through the seam of his jeans | cock · cunt · wet · suck · fuck | full — cunt, cock, cum, throat, fuck, come in her |
| `npc_wes` | tits · ass · dick · hard | cock · cunt · fingers in her · fuck | full — cum, throat, ass |
| `npc_simone` | tits · ass · wet · what she calls Josie in front of the others | cunt · fingers · tongue · come | full — cunt, cum, slut, and the words she uses about Josie to men |
| `npc_halloran` | hard · his cock · the word *cunt*, and it is his word | cock in her mouth · throat · cum | full |
| `npc_dee` | **none — she is heard through a wall, never touched.** A deliberate ceiling, not an omission. | none | none |

- **Where the crude register lives — the repeatable surfaces, by name:**
  1. the upstairs at the pledge house on a party night
  2. the shared bathroom at the Kessler house
  3. Halloran's office hours
  4. the Friday dues count
  5. the back room of her campus job

  Not one of these is a one-time scene. If the crudest writing in this game ends up in a scene the
  player sees once, the game is already cold.

---

## The four checks

1. **What does release 41 add?** `reputation` 85 — the other house on the row, whose people arrive
   already knowing her. Answered against a named tier.
2. **What can she reach at the top that she cannot at the bottom?** The upstairs on a party night,
   the office after hours, the kitchen at one in the morning. §3.
3. **Which character would a player miss if deleted?** Simone. She is the only person who decides
   who Josie is allowed to be, and she is the one who bills her for it.
4. **Which repeatable surface carries the crudest writing?** The upstairs at the pledge house on a
   party night — re-entered, cycling, and it is where `nerve` and `reputation` both cash out.
5. **`gates.py --words`** — run below, list read.
