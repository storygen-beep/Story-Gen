# SCENE · Mercer — the walk-in  `[READY]`

`walkin_mercer` · **`substitution_only = true`** · target of `trigger.substitutions` on
`loop_mercer` and on the penthouse's `Sleep here` row

⚠️ **Gate `the walk-in floor` reads BOTH his rooms** — he is scheduled at each and she has solo
rows at each.

```
the router    trigger.substitutions on the ACTIVITY, chance x conditions, rolled on entry
the branch    ONE canvas, substitution_only = true, [group] bands on `service`
the payoff    routes into loop_mercer, a rung that already exists
```

| band | chance | what happens |
|---|---|---|
| `service lt 20` | 0.15 | Somebody is shown in while she is still in the room and Mercer does not send her out. |
| `service gte 20, lt 45` | 0.40 | He offers her to the man he is meeting, in the tone of offering a drink. |
| `service gte 45` | 0.70 | The man has clearly been told what she is before he arrived. |

**Same button. He is not escalating — the room is filling up.** The odds ride `service`, and the
content rides who else is present, which is the same axis `loop_mercer` bands on. **One character,
one axis, two surfaces.**

⚠️ The low band is not an act node; the high band routes into `loop_mercer`, whose three bands carry
the floor by construction.

⚠️ **The target MUST declare a `location`** (`v2.py:3177`). This one is declared at `penthouse`;
the stall's traffic uses the `priced` band inside the loop rather than a second walk-in canvas —
**one per ROOM, not one per pair**, or the cross-product becomes the wall of buttons one layer down.
