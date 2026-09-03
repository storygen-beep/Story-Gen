# PLACE · Spire Plaza  `[READY]`

| | |
|---|---|
| **id** | `spire_plaza` |
| **ENTERED FROM** | `the_street` |
| **WAYS OUT** | `vance_securities` · `penthouse` · back to `the_street` |
| **DOOR** | no — a public forecourt |
| **LABELS** | `outdoors` · `public` · `zone:spire` · `checks_cover` |
| **fill** | 800 `[INTENT]` |
| **heat** | cold |

## What this place is FOR

**The first door that reads her.** Glass, badges and a lobby that decides whether she is staff.
Nothing happens here; what happens is that she is *let through* or not, and that is the `cover`
tier's first consequence surface.

## The list

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Through the lobby." | `TBD` | exit | `cover` | `cover gte 10` **and** `clean gte 40` | `time` `add` `+10` | yes |
| 2 | "Back down the hill." | `TBD` | exit | — | — | `time` `add` `+20` | yes |

## The refusal (SY5 · R5c)

⚠️ **The refusal is a SENTENCE, not a greyed label.** Vesper shipped **4 of 13 shown-locked choices
with no reason at all** — 30% mute against the field's 2%. Each refusal here names which of the two
terms failed, separately, the way `become-taxi-driver` names every unmet term with directions:

- under `cover 10` — the desk looks at what she is wearing and says the thing it says to couriers
- under `clean 40` — it is not the clothes, and he does not say what it is

`locked_text` carries it. Not `show_when_locked` with a bare label.
