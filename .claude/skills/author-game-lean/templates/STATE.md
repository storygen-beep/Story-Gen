# STATE: <game title> (<slug>)

<!-- Keep this under 100 lines: a digest, not an archive.
     Update it in the same turn as every build, because a stale state is worse than none (C2040).
     Store only what can't be worked out from the game: what was decided, what's owed, what was promised.
     Counts, scene lists and check results come from check.py, not from here (C2041).
     When a release ships, its piece rows collapse into its one-line record under Shipped
     (what shipped, the date, the commit). Only the current release's pieces stay as rows. -->

## Built

- <person / place / system>: <one line on what it is now>

## Release <n>: <name>

Out of scope: <what this release leaves for later>

| piece | what | approved | built | checked | played |
|---|---|---|---|---|---|
| <id> | <one line> | <date> | <date> | <date> | <date> |

## Open

- <what's owed or promised> (from <piece id or NOTES line>)

## Shipped

- <release> · <what shipped> · <date> · <commit>

Next step: <plan|piece|build|release> — <what>
