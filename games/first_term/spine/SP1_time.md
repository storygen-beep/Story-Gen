# SP1 · Time — First Term

> [READY] · drafted 2026-10-03 · updated 2026-10-07 (the drinks boost line) · signed by LO: LO, 2026-10-07
> A decision record, ≤ 400 words. The rules: `references/the-spine.md` SP1 · `the-clock.md` · `engine.md` §28.

| decision | answer |
|---|---|
| starting day and hour | Monday, 07:00 — her first morning of college (`[time] starting_hour`; the only hour the prose may name, `the-clock.md` C1) |
| a day in play is about | 15–20 minutes of play |
| canvases that run past midnight | parties at Zoe's apartment (to about 02:00) · Ryan's room, late at night. A window past midnight needs a second schedule entry on the next weekday. |
| schedules | lectures and café shifts each keep their own hours and may overlap; the player picks what to do. Three classes a weekday, two in the morning and one in the afternoon, Friday one (`SYSTEMS.md` §1, LO 2026-10-07). No hours are set here: the café's come with its system card, the lectures' with the college card. |
| the rent | taken by the engine at 00:00 on Sunday (`[settings.rent]`, `engine.md` §26); Mark's kitchen-table scene sits beside the payment, never on it. It starts after the scene where Mark tells her she pays rent now (`start_after_flag`, LO 2026-10-07). |
| how the prose treats time | `the-clock.md` C2 and C5: a beat never reads the clock. A rule of the world may name an hour (C2's exemptions, e.g. "Claire picks him up at 7:30"). A blocked row shows its hours on its `cooldown_message`. |

**The overnight list** — what `[engine.daily_tick]` clears or moves at midnight (the day rolls over in `v2.py:6806-6808`):

| flag or trait | what happens overnight | why |
|---|---|---|
| `ryan_hall_today` | cleared | the morning bathroom meeting can happen once a day |
| `cafe_shift_1_today`, `cafe_shift_2_today`, `cafe_shift_3_today` | cleared | up to 3 café shifts a day (LO, 2026-10-03). The café row's choice sets the first one not yet set, and is gated on that flag being false; with all three set, the row shows "no more shifts today". Flags, not a counter (`engine.md` §28: "Use a flag; flags are not meters"). |
| the drinks boost (`drinks_boost`) | not on the tick | a timed modifier that runs out 3 hours after the last drink (`v2.py:6810-6820`), so it never vanishes mid-party. It lifts her choices only; steps ignore it: a step's gate adds "`drinks_boost` is not active" (the modifier condition, `v2.py:4993-4998`; LO, 2026-10-07). SP2 §1's "clears overnight" (`SP2_ladders.md:29`) means it is gone by morning (LO, 2026-10-07) |
| `hygiene` | falls a little | `[player.trait_decay]`, every night; with `hygiene_off` (the start choice) nothing reads it (`engine.md` §30.1; LO, 2026-10-07) |
| `energy` | not on the tick | refilled by sleeping in her bed, a scene; listed so nobody adds it to the tick (LO, 2026-10-07) |
| `laura_rule_ryan_first` | kept | it is a house rule once Laura makes it |
| the short-Sunday knock flag | kept | cleared by Vance's knock scene, not overnight; listed so nobody adds it to the overnight clear (`LIVES.md:274`) |
| every person's meters (want, warmth, power) and step counters | kept | they move only through scenes |

**Flags that cross midnight are never cleared by the tick** (LO, 2026-10-07). The tick runs at
midnight, not when she sleeps (`v2.py:6806-6808`). Ryan's skip-Kayla and cancel-Kayla flags, the night
both parents are away and Laura's weekend away are read by hours since they were set (`engine.md` §52),
or cleared by a scene.

**Not decided here:**
- lecture hours — the college card;
- her needs: energy and hygiene, no hunger (`SYSTEMS.md` §5–6, LO 2026-10-07);
- Ella's meters: decided on SP2 §1 (Corruption and Exhibitionism).

**The party** (not on the overnight list, 2026-10-06): the party happens only on Friday. Its start is
gated on the Friday evening row, so it can't start again after midnight, when the day reads Saturday.
Arriving sets `party_went`; the after-midnight part stays open by reading `hours_since_flag` on that
flag, so midnight never splits one party into two.
