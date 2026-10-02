# [REVIEW] Place — <location name>

> One page. Rules: `references/the-sheets.md` S1–S4, S6, S9 · `the-surfaces.md` R2.
> Saved at `games/<slug>/sheets/places/<location_id>.md`.

| row | answer |
|---|---|
| kind | `thoroughfare` · `destination` |
| ENTERED FROM (S2) | <location_id> |
| labels — what kind of place | <label, label> |
| hours (`hours`, `closed_text`) | <weekdays, open–close — or "always"> |
| hidden until (`hidden_until`) | <flag — or "no"> |
| fill — word budget (S3) | <a round number> |
| door | <yes: who answers — or no> |
| dress code or wanted state | <`clothing_rules` slots, or a `worn_*` state in `entry_conditions` — or "none"> · <the reason she is told> · <the way out: change · what to buy> |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| <canvas> | <npc · days · hours> | <action> | <location> |

## Rows (`serves`)

| row | kind (need · work · person) | system it surfaces | cost and effect, with op (S4) | BRAKE (S9) |
|---|---|---|---|---|
| <label> | <kind> | <system id> | <trait op value> | <trigger cost · per-day cap · day flag> |

## Why — the source of each key choice

A rule (its file and id), a scout card, LO's call (with the date), or **guess**. Writing "guess" is
allowed; hiding one is not (`references/the-release.md`, "When LO rejects something").

| key choice | source |
|---|---|
| <what it hangs off · its labels · its hours · its door> | <rule file + id · `scout/<topic>.md` · LO, <date> · guess> |
