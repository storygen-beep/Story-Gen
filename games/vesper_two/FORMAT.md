# FORMAT — the row shape for Vesper: Undertow

Per-game notes on the shape of a sheet. `the-sheets.md` owns the rules; this file only fixes the
things that file leaves to the game, and it fixes them for one reason.

## Why this file exists

On 2026-09-03 a sheet-versus-build check was designed, costed and dropped. The reason was not that
the check is hard — it is that the artefact it would read does not exist:

- 2 of 33 games have a `sheets/` directory at all
- the two that do use incompatible formats — markdown tables against fixed-width ASCII in `<pre>`,
  where a row is told from an annotation by 2-space against 6-space indentation
- **of 43 row cells across `orientation`'s twelve tables, zero contain a backtick** — so joining a
  sheet row to a canvas needs fuzzy name matching
- four typographic markers change what a row means (`**bold**` is a row, `├ *italic*` is not,
  `~~struck~~` is deleted, `*(walk-in)*` is an ambient) and ignoring them miscounts 6 of 12

Its own verdict: *"it becomes an instrument when sheets are corpus-wide and a row names its canvas;
both are cheap to do while writing, and neither is worth retrofitting to 31 games."*

This game starts fresh, so it pays that price now.

## The two rules

**1 · Every row names its canvas id, in backticks.** Not the button label, not a description — the
id the TOML will carry. A row with no id yet writes `` `TBD` `` and that is a visible debt.

**2 · Meaning lives in a column, never in typography.** No bold-means-live, no strike-means-cut, no
italic-means-not-a-row. Every row carries an explicit `kind`, and a cut row is deleted or its kind
says `cut`. This is the direct fix for the miscount above.

## The row

Place and person sheets use one table shape:

| col | holds |
|---|---|
| `#` | row order as the player sees it |
| `row` | the button label, quoted exactly as it will ship |
| `canvas` | `` `canvas_id` `` — or `` `TBD` `` |
| `kind` | `hub` · `act` · `work` · `need` · `walkin` · `ambient` · `exit` · `door` · `cut` |
| `system` | which declared system this row belongs to, by key. `—` is a finding, not a blank. |
| `gate` | the condition, with trait, op and value |
| `effect` | trait, **op** and value — `op` is never omitted (S4) |
| `screen` | `yes` / `toast` — does clicking land on a screen (`the-surfaces.md` R9) |

## Counts

Every count on a sheet is marked **`[INTENT]`**. There is no `--sheets` mode, so nothing here has
been produced by an instrument. A number becomes a measurement when `gates.py` prints it and not
before (S1).

`beat` on any sheet means **one node**, which is what `gates.py` counts. A node holding three
explicit paragraphs is one explicit beat, not three.

## Status

Status lives in the document title, never in a separate tracker:

```
[REVIEW]    written, waiting on LO
[READY]     LO has read and signed
[GAME-READY] built and reconciled against the build
```
