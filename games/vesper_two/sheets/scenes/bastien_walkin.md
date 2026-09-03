# SCENE · Bastien — the walk-in  `[READY]`

`walkin_bastien_backroom` · **`substitution_only = true`**

⚠️ **His place sheet declares this NOT gate-required** — his rows are a door and a hub, no solo
work — **and that is an unverified claim.** If the gate counts the door canvas as a solo activity it
will fire. It cannot be checked until a build exists, and it is logged rather than assumed away.

Built anyway, because the door search already does the walk-in's job better: it fires **every
visit** and bands on `seated`, which is *one activity deepens* rather than *the room widens*.

| band | chance | what happens |
|---|---|---|
| `seated lt 2` | 0.10 | Somebody is at the bar door waiting to talk to him and he does not hurry. |
| `seated gte 2` | 0.30 | He calls the man in to look at what the search turned up. |

⚠️ **The target MUST declare a `location`** (`v2.py:3177`).
