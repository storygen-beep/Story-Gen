# PERSON · Simone  `[READY]`

| | |
|---|---|
| **id** | `npc_simone` · **fixed name** |
| **role** | the senior who runs the pledge house — **role before name**: the player meets *the woman with the sign-in book* |
| **home** | `the_pledge_house` |
| **meters** | `relation` (access) + `lust` (willingness) — the rich pair, because she carries an arc |
| **met** | `the_pledge_house`, **Mon 16:00–19:00** · flag `met_simone` |

**Why she is wanted:** she decides who Josie gets to be on that campus and says so out loud. **Being
chosen by her is the fantasy; being billed by her is the engine.**

**What she owns:** the pledge ladder, the other girls, the party, and **the dues**. She is the
collector — a woman, on campus — which is the inversion the whole game runs on.

---

## The schedule grid

| # | location | start | end | weekdays | activity |
|---|---|---|---|---|---|
| 1 | `the_pledge_house` | 16:00 | 19:00 | `[0,1,2,3,4]` Mon–Fri | the office, and on Friday the book is open |
| 2 | `the_pledge_house` | 21:00 | 23:59 | `[3,4,5]` Thu–Sat | downstairs, then not downstairs |
| 3 | `the_pledge_house` | 00:00 | 02:00 | `[4,5,6]` Fri–Sun | still up |

⚠️ **Rows 2 and 3 are ONE party window split in two.** Day-specific, so it must be two rows: a
`[3,4,5]` row running 21:00–02:00 would put her there on Thursday night and **delete her at
midnight**, because `todayIndex` is Friday by then and the weekday check runs first (`v2.py:3596`).
The `[4,5,6]` on row 3 is Thursday-night-becomes-Friday, Friday-becomes-Saturday,
Saturday-becomes-Sunday.

⚠️ **The Friday dues sit inside row 1**, at the desk, in person. She is the face on the obligation —
a date and a face are what turn *you could work* into *Friday, $120, or else.*

---

## The arc — 7 steps, direction **THEIRS**

`the-arc.md` A5b. What is gated is **the house's willingness**, not hers. She is the one asking, and
what the arc climbs is whether they will have her — which means **the refusals here are theirs, not
hers**, and until A5b nothing in this skill said that was a legitimate shape rather than a slip.

**A2 — steps 1–2 carry no sex.** They buy **when she is alone** (the office, after six, when the
house is empty of everyone but her) and **what she is vulnerable about** (the house is two girls
short and the row is watching).

| # | step | gate | what it teaches or takes |
|---|---|---|---|
| 1 | sign the book | `met_simone` | the window, and the fact that nobody reads it |
| 2 | the house is two short and she says so | `simone_01` · relation 8 | **what she is vulnerable about** |
| 3 | the first dues, and what being short would mean | `simone_02` | the obligation, armed after income exists |
| 4 | **the refusal** — she is asked upstairs and does not go | `simone_03` | **A3b: PARKED** — *Thursday, after nine* |
| 5 | **wear it** — the arc will not pass until she does | `simone_04` · `worn_exposure` | **A6 — a garment is a rung.** She does nothing; she wears something |
| 6 | the first party she is not standing at the edge of | `simone_05` · `nerve` 30 | |
| 7 | **conversion** — *Go up* appears on the room list | `simone_06` · `reputation` 25 | sets `simone_open` |

**Step 5 asks her to do nothing at all.** It asks her to *wear* something, and lists what qualifies.
`worn_exposure` is the predicate, and it is the only one of the four worn predicates that reads an
empty slot. **What money buys opens a door** (R1b): the outfit is bought at a price and read here.

⚠️ **A5b's saving and its risk.** One template stamped per person is a normal way to build a cast —
Zara runs nine arcs off one shape. The risk is that they read as one character repeated. Ray's arc
and Simone's share **no acts, no refusal shape and no aftermath**: his is hers-climbing and parked
in a kitchen; hers is theirs-climbing and parked on a staircase.

---

## The converted surface — `the_pledge_house` · *Go up*

**This is the anchor's act surface and the crudest writing in the game lives here** (Want §7). It is
re-entered, not seen once — which is the correction this whole system exists for. The measured
failure wrote its explicit register only into content the player sees once and wrote its
fifty-times-replayed loops as literary character study.

**BRAKE:** `trigger.costs rest 15` · day-cap `went_up_today` **on the choice** · Thu/Fri/Sat window.

**Text varies on re-entry** — `block_pool` for undirected variety, stacked `group` bands on `nerve`
for directed. Zero v2 games have ever used `block_pool`; this one does.

## Crude ceiling

| tier 1 | tier 2 | tier 3 |
|---|---|---|
| tits · ass · wet · what she calls Josie in front of the others | cunt · fingers · tongue · come | full — cunt, cum, slut, and the words she uses about Josie to men |
