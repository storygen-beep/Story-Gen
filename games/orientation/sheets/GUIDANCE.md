# GUIDANCE — quest cards  `[READY]`

**S10 — guidance has a row, and it is written NOW, not after the first gate run.**

> **The incident.** `quests_engine = "v2"` lights a sidebar entry and a page, and with no cards it
> renders **a heading and nothing.** No sheet in that format mentioned a quest card; nine were
> written from scratch after the first gate run.

**Lostness is the genre's dominant complaint** — a **4.7%** median share of player comments against
grind's **0.9%**. It is not a polish item.

---

## One card per ascent tier

`the-voice.md` R2 — every ascent tier carries a visible ladder.

| tier | card | `when` | goal |
|---|---|---|---|
| `nerve` | *Let them look* | `met_simone` | reach `nerve` 30 — names **where**, not the number |
| `appetite` | *Ask for it* | `ray_03` | reach `appetite` 30 |
| `reputation` | *Be talked about* | `met_simone` | reach `reputation` 45 |

⚠️ **R3 — name the FEEDER, not the number.** A card that says *reach nerve 30* tells the player a
number they cannot see. The card says **where to go and what to do there**: *the house, on a
Thursday, and do not stand at the edge of it.*

---

## One card per character

| character | card | `when` | closes on |
|---|---|---|---|
| `npc_ray` | *The kitchen after she's gone* | `met_ray` | `ray_09` → then a standing card, never silence |
| `npc_simone` | *The book by the door* | `met_simone` | `simone_06` |
| `npc_wes` | *One bathroom* | `met_wes` | relation 30 |
| `npc_halloran` | *The eight o'clock* | `met_halloran` | relation 30 |
| `npc_dee` | — none. She is the price tag, not a route | | |

⚠️ **F8 — the same flag belongs on that character's quest cards.** `met_<x>` gates both the portrait
and the card, so a card never points at somebody the player has not met.

⚠️ **R5 — nothing retires into silence.** Gate *no chain ends in silence*: every character ladder
keeps a card after its last rung. Ray's becomes a standing card once `ray_09` fires, because the
surface it opened is repeatable and the player has to know it is there.

---

## Two engine traps

⚠️ **Quest cards take FIVE operators, not six.** `[[quest_cards]]` `when` and `goals` reject `ne` at
build time, deliberately — their evaluator has no case for it (`engine.md` §37). Canvas, node and
choice conditions take all six. **Do not widen that whitelist without the evaluator case in the same
change.**

⚠️ **The badge arrives before the content.** Frame 1 fires on `terminal === true` **alone**, ahead of
ready and goals, and nothing checks achievement. A ✓ that lands on the last content reads as *done*
while content is still there. **Put the ✓ on a FLAG the content sets on its way out**, so it means
*you played this* — not on a meter threshold.

---

## The wall and the card are different jobs

**R4 — a wall shows the want; the card shows the route.** The locked row is now `act_row_walk`'s
*stop when she says your name* at `the_row` (`reputation 85`): it says what she wants and what bars
it. The **card** is what tells her where to go and earn it.

⚠️ **AND THE CARD WAS POINTING AT A SPENT LEVER.** The 25→85 reputation card carried
`ready_canvas = "act_quad_wall"`, and that activity's grant is capped at 45 — so for the entire
second half of the climb the game's own compass sent the player at a button that could not move the
goal. `gates.py` had the right answer and printed it every build: *"cheapest rung
act_pledge_upstairs +5 / 30 min"*. Repointed 2026-09-02. **A card whose `ready_canvas` cannot reach
its own goal is worse than no card.** Ours is the corpus's best shape: a refusal that names **every unmet term separately,
with directions**, rather than one greyed label.
