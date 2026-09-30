# [REVIEW] System — energy

| row | answer |
|---|---|
| kind | ambient: the body's clock |
| the key it keeps | `energy`, 0–100 |
| fed at | her_room (sleep); house (eat, +10) |
| room labels it attaches to | she_can_sleep |
| what reads it | below 20: no shift, no bus downtown |

## Where it surfaces

| room | row label | reads (op, value) | what the player sees |
|---|---|---|---|
| firm | Work a shift | energy gte 20 | greyed: "Too tired to work (need 20 energy)" |
| linden_street | Take the bus downtown | energy gte 20 | greyed, with the need |
| her_room | Sleep | — | energy set 100; the clock moves 8 hours |

Costs: a shift, energy add −30. A night downtown, energy add −20.
