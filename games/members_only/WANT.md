# The Want — Members Only

> Re-read before every release; bump `want.last_read_at_release`. Doctrine: `references/the-want.md`.
> The fantasy, the model to beat and the promise are on the idea page (`IDEA.md`, next step).

**Everyone in this game is an adult.** She is 24 · Dana, her sister, 29 · Julian 46 · Ade 34 ·
Kessler 63 · Noor 27. Every member, staff member or passer-by added later gets an age here first.

## 1. Who the player is

- **Who:** `female`. **Written or blank:** `blank`, but her situation is fixed (Dana's younger sister).
  One creation field, her first name, printed back on every screen where Julian doesn't call her Dana.
- **Start choice — a memory, not a slider.** At the staff door, Noor asks the question the scene is
  already asking: *"So why'd you and your sister stop talking?"* Three answers, one flag each:
  `past_same_man` (they fought over a man) · `past_she_left` (Dana walked out on her) ·
  `past_you_left` (she walked out on Dana). Each flag swaps a line with Ade, Julian and on each diary page.

## 1b. Who she is

Twenty-four, broke, and eight months without a word from Dana. Dana worked at **the
Linden**, a members' club on the cliff above a harbor town, and stopped answering in May. Her last
letter: *"Don't come looking."* So she came, and she took Dana's old job.

**What she has to lose:** her own name and her own body's limits — the club wants a second Dana.
**What holds her here** (`hold_kind = bill`, collector `julian`): Dana left owing the club, and Julian
puts it on her — **"Dana's tab", $300 every Sunday**, counted at his desk. It never runs out. Miss it and
she is off the floor and shut out of the rooms upstairs for the week; the game does not end. Julian
also keeps the key to the staff house. No date: the pressure repeats (`SKILL_TEST_FINDINGS.md` #14).

## 2. The appetite

**To be the one the whole room asks for by name — and to know everything the men at the Linden
know.** There is always one more member, one more locked room, one more thing they know.

**Where the hold stops being the reason:** the night she climbs the stairs to a member's room with no
page on offer and no rule that sends her — because she wants to be asked.

## 3. What she is becoming — as access

**Bottom:** she carries trays on the bar floor and the terrace, sleeps in the staff house, and walks the
town on her afternoon off. Every door upstairs is shut to her.
**Top:** she has the run of the members' floor, the library after hours, Julian's office and the boats
at the docks; she is booked by name, and members hand her what they know without being asked.

| tier key | what going further means | early rungs | late rungs |
|---|---|---|---|
| `shown` | being looked at — the terrace, the pool, the dress, the table she dances on | the short dress; the pool at night | a member's table; the stage on a party night |
| `favour` | what she does for a member in his room | a drink in his room; his hands | the whole night; two members at once |
| `nerve` | going where staff are not allowed | the service stairs; the book behind the bar | Julian's office; the members' book |

Rung numbers are set on the board (`the-meters.md` W4), not here. **No counterweight** for now.

**What does release 41 add?** A new member holding a new diary page, whose surfaces open on the upper
`favour` rungs, and a new room upstairs that the upper `nerve` rungs get her into.

## 4. The charge

**Transformation**, turning into **Reversal**. She comes to pull Dana out and becomes the next Dana; late,
what Dana wrote down gives her power over the man who holds her sister's tab.
**§4a:** Julian collects the hold and is *not* the pipe the sex comes down. The heat comes from the
members and from Ade. Julian is the one she cannot face — the late, deniable target (§4b).
**§4b:** she wants it and goes to get it. The pages give her a reason to walk upstairs the first time,
not every time. The design is what stops her: Julian's rules and his Sunday count, Julian's eyes, the locked doors.

## 5. The world

**Where:** a harbor town and the members' club on the cliff above it, open all year; members come and go by boat.
**Outside her door:** the staff house sits halfway down the cliff path, between the club and the docks.
**How far she can get:** the town and the beach on foot. The boats and the next town need a member.
Dana's tab means she can't just leave: walking out leaves Dana's name on the debt and her own questions unanswered.
**Shape:** `nested_zones` — the town (docks, café, beach), the cliff path, the club (bar floor, terrace,
dressing room, library, members' floor, Julian's office), and the staff house.
**Needs:** `sleep` — exhausted means Julian sends her home, no shift and no upstairs.
`look` — hair and dress undone means she's not allowed on the floor. Both shut the club's doors.
**How alive:** a living world. Members arrive and leave by the boat schedule; staff keep their shifts.

## 6. Why this person

| character | why they are wanted | what he visibly wants (A13) |
|---|---|---|
| `julian` 46 | the man who made Dana; being wanted by him is being told she's better | her as Dana — he calls her Dana once and doesn't correct it, and has Dana's dress altered to fit her |
| `ade` 34 | the one man here who looks at *her* | her, and it scares him — he pours her drink before she asks, every shift |
| `kessler` 63 | old money, filthy, honest about it; holds page one | her reading aloud, standing — each page she reads, he asks for more |
| `noor` 27 | one step ahead of her; the companion and the rival for Dana's old place | Dana's old place — she times every shift against hers |

## 7. Register

- **`narration_person`** = `second`.
- **Crude ceiling** (words, not a mood):

| character | early | middle | late |
|---|---|---|---|
| `kessler` | tits, ass, "good girl" | cock, cunt, "spread" | come on me, "on your knees" |
| `ade` | "god, look at you" | cock, pussy, fuck | cunt, "come for me" |
| members | tits, ass | cock, fuck, suck | cunt, cum, whore |
| `julian` | nothing crude — he speaks like a bill | "your body is the job" | cunt, once, late |

- **Where the crude register lives:** the repeatable surfaces — a member's room upstairs, Ade's bar
  after close, and the library readings. Never only in one-time scenes.
