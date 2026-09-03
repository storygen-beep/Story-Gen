# SCENE · Kess 2 — The rate  `[READY]`

`arc_kess_02` · `kess_berth` · 10:00–22:00 · gate `kess_met` · `coin gte 10` · sets `kess_tenant` ·
**no sex**

## What this step ARMS

⚠️ **This is where the obligation switches on.** Until `kess_tenant` is set the feed line does not
exist. `the-economy.md` R3: **armed after income exists** — pressure before she has a way to earn is
a scripted loss, not a choice. She lands with under ten coin, so the first thing the game does is
name a price she has not got and the second is point her at the floor that pays.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_rate` | Ten a night, his terms, and it buys the charge and a few days of his attention. He is not cruel about it. He is a man with a bench and a rate. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Take the terms." | `kess_tenant` set · `relation` `add` `+2` | yes |
| "Ask what the attention is for." | `kess_tenant` set · `relation` `add` `+4` | yes |

⚠️ **The charge itself is NOT here.** It is `costs = { coin = 10 }` on the bench's night row, which
is the single authored outflow gate 24 compares `obligation_amount` against (`gates.py:5901`).
`[settings.rent]` is unused — `due_day` takes weekday names only and arms at 00:00, so the engine's
system is weekly and cannot express a nightly demand.

## Media

`videos/locations/kess_berth.jpg`.
