# [REVIEW] Coverage — <game title>

> One page, one table: every topic this game needs, and what the skill really knows about each.
> Rules: `SKILL.md` Operating rules ("Never build an unknown on a guess") · `references/the-sheets.md` ·
> `state.md` (`board.coverage[]`). Saved at `games/<slug>/sheets/COVERAGE.md`.
> Written at the start of the `spine`-phase world work, before the system cards and the rooms; topped up
> each release with anything the release adds that is not on it. Recorded as `board.coverage[]`, one
> entry per row.

**A topic** is one of four kinds, never a single canvas:
- `system`: one per `board.systems[]` card (a job, a shop, the rent);
- `place`: a kind of place (a home, a bar, an office, a club);
- `scene`: a recurring scene type (a date, a party, a shift, a sleepover);
- `mechanic`: something the game leans on (a bill, a review, a deadline, a reputation).

**A status**, and the source each one needs:
- `covered`: a skill rule or card exists. The source names it: the file and rule id, or the card file.
  A rule *near* the topic is not enough.
- `scouted`: no skill rule; a scout card exists. The source is its path, `games/<slug>/scout/<topic>.md`.
- `lo`: LO decided it. The source quotes him, or gives the date.
- `placeholder`: built thin on purpose. The source is the release page line that names it as unfinished.
- `unknown`: nothing yet. It is not built until it takes one of the four above.

## The list

| topic | kind | status | source | note |
|---|---|---|---|---|
| <topic> | `system` · `place` · `scene` · `mechanic` | `covered` · `scouted` · `lo` · `placeholder` · `unknown` | <file + rule id · `templates/cards/<card>.md` · `games/<slug>/scout/<topic>.md` · "LO, <date>: <quote>" · the release page line> | <one line, or blank> |

## Unknowns, for LO

The build session lists every `unknown` here and asks. It never runs a scout on its own. A scout that
comes back "not found" returns here, never to a guess.

| topic | what LO wants: scout it · decide it · a placeholder | LO's answer (date) |
|---|---|---|
| <topic> | <scout · decide · placeholder> | <answer> |
