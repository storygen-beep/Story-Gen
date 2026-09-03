# SCENE · Colm — the walk-in  `[READY]`

`walkin_colm_backroom` · **`substitution_only = true`** · target of `trigger.substitutions` on
`underworld_bar`'s floor rows

⚠️ The anchor's walk-in is declared on `underworld_bar.md` and bands on `service`. **This one is
Colm's**, bands on `colm_drinks`, and fires only once `colm_open` is set — one per ROOM is the rule,
and these are two different activities at one room rather than a cross-product.

| band | chance | what happens |
|---|---|---|
| `colm_drinks lt 3` | 0.10 | The delivery he is waiting on arrives and he leaves her mid-sentence. |
| `colm_drinks 3-5` | 0.30 | He brings the man he is drinking with into the back room to finish the story. |
| `colm_drinks gte 6` | 0.55 | He forgets she is behind the crates and lets the room in. |

**Same button. He gets less careful as the night goes, and so does the room.**

⚠️ **The target MUST declare a `location`** (`v2.py:3177`).
