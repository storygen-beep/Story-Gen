# PLACE · The Row  `[READY]`

| | |
|---|---|
| **id** | `the_row` · button `The Row` |
| **ENTERED FROM** | `the_quad` |
| **FILL** | 400 words |
| **cycling pool** | no — cold on purpose; the heat on this side is inside `the_pledge_house` |
| **DOOR** | **no.** It is a street. The doors on it belong to the houses, and seven of those houses are 0.2 |
| **LABELS** | *(none declared — `board.systems[]` has not been taken)* |

⚠️ **This replaces `act_quad_row`, and the difference is the whole point.** That canvas was 0.1's
declared locked door: gated at `reputation >= 85`, its only content its own `locked_text`, and its
reward branch returned the player to `the_quad` after thirty minutes with **no effect, no flag and
no destination**. `gates.py` printed it every build — *"costs 30m and leaves nothing behind"* — and
it shipped anyway, because that check is a lint. A playtest asked what the button was for. It was
for nothing.

⚠️ **Open, not locked.** A locked street with nothing behind it is the same defect wearing a new
costume: grind four to six in-game weeks to 85, walk in, find an empty road. So the row is walkable
from the first visit and **what 85 buys is being spoken to on it** — see the list below.

⚠️ **R4 NAMING RISK, ACCEPTED IN THE OPEN.** `the-map.md:180-183` killed **`The Parade`** for being
a word a player cannot resolve off a button. *"The Row"* is the same class of word. It survives
because the game teaches it before this card exists — the meeting with Simone, the dress on the rail
at the union shop, the sidebar band *"The row knows who you are"*, 17 prose sites — and because R4
puts the load on the **location's own description** where the button cannot carry it. **Its first
clause says "eight houses" for exactly that reason.**

## What kind of place this is
Eight sorority houses along the east edge of the quad, porches all facing the same way. She has been
inside one of them — the third, Simone's — and the other seven have their own books by their own
doors and their own Fridays. It is the ground `0.2` opens into.

## The list
| row | system |
|---|---|
| **Walk the row (30m)** | ascent — `reputation`. Open at any level; the prose bands at 45 and 85 |

The gated exit, `Stop when she says your name.`, is the reputation tier's **only** `gte` site in the
game. Deleting `act_quad_row` took gate `ascent tiers expand the world` **red** — reputation at 0
expand / 0 contract, a declared tier gating nothing. This carries it now, and it pays in the
currency the meter is about: somebody uses her name **first**. Sets `row_knows_her`, and costs
`home_face` — being known on that street is exactly what the household is not supposed to hear.

## What the street reports
Three `description_variants`, first-match, banded on `reputation`:

| band | what the row is doing |
|---|---|
| **85+** | two porches stop talking as she passes and start again after; the second uses her name |
| **45–84** | somebody lifts a hand without stopping what she is saying; a car goes past slowly |
| **25–44** | their own books by their own doors; she knows two names and neither knows hers |
| *base* | eight porches, four with people on them, and the conversation does not change shape |

## Ways out
`the_pledge_house` · **back → `the_quad`**
