# SCENE · Renner 1 — Cheap hands  `[READY]`

`arc_renner_01` · `renner_depot` · Mon-Sun 09:00–18:00 · gate: — · sets `renner_hired` · **no sex**

## Nodes (one node is one screen)

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_hired` | He is hiring hands and does not look at the one he hires. He says what the work is and what it pays, and nothing else. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Take it." | `renner_hired` set · `relation` `add` `+2` | yes |
| "Ask what happened to the last one." | `renner_hired` set · `relation` `add` `+1` | yes |

⚠️ **Both arms set the flag.** A refusal here would strand the arc before it exists; the choice
colours the entry, it does not gate it. `the-surfaces.md` R5 — 35% of the field's conditionals are
variant selectors where every branch offers something, against 23% that refuse anything.

## Dialogue

**Somebody speaks.** He does — this is the meeting's follow-on and F6's bar applies. Field median
narration-to-dialogue is 2.93:1.

## Media

`videos/locations/renner_depot.jpg` — on disk. No `_t` slot; this beat is not explicit.
