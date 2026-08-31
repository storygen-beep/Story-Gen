# [REVIEW] The Front Desk

## In short

- **The anchor.** Most of the game's prose lives here and it is where she stands all night.
- **Five things to do** — field median for a place is 3, engine backstop is 8. The anchor sits above
  the median on purpose.
- **The camera monitor is here, not in the office** — moved while writing this sheet, and the reason
  matters: it is the corruption on-ramp and it cannot sit behind a door that is locked two nights
  in three.
- **Five ways out**, because this is the hub and every need pulls her off it.
- One thing I am unsure of, at the bottom.

---

<pre>
THE FRONT DESK                                        id: <a href="the_desk.md">the_desk</a>
release 1 · authored 5 · player sees 3–6 · cap 8      ANCHOR

DOOR         free · always open — the shift starts and ends here

INSTEAD OF THE SCREEN
  ⚡ first_shift              ONCE · night 1 · the boot
  ⚡ del_handover             ONCE · after first_shift, Del's hours
  🎲 a car pulls in          1 in 3 · 18:00–01:00      1 in 8 · 01:00–06:00
  🎲 the phone               1 in 6 · any hour · 2-night cooldown
  🎲 nobody at all           1 in 5 · 02:00–05:00 · only when the lot is under 3 cars

THE ROOM SAYS
  base              Two fluorescent tubes over the register, and one of them ticks.
                    Twelve keys on twelve hooks. The monitor cycles four cameras at
                    eight seconds each.
  ~ after 02:00     ...the road has been empty for an hour and the tube is still ticking.
  ~ daylight        ...the glass is doing nothing to keep the heat out, and everyone
                    who walks past can see straight in.
  ~ exhibitionism 30+   ...you stopped sitting behind the counter about a week ago.

WHO IS HERE
  Del        22:00–02:00, about 1 night in 3     → see <a href="../people/del.md">del</a> sheet
  Marek      00:20–01:30, on his way for ice     → see <a href="../people/marek.md">marek</a> sheet

THINGS TO DO
  Take the check-in                              20m   +$6      only when someone is waiting
      ~ exhibitionism <12    you keep the counter between you
      ~ exhibitionism 12+    you come round the side of it to hand the key over
  Watch the monitor                              15m   ONCE A NIGHT
      ~ corruption <20       four empty corridors and the ice machine
      🎲 1 in 3              there is something on camera two
  Run the audit                02:00–04:00       45m   ONCE A NIGHT
  Walk the property                              20m
  Make coffee                                    15m   +energy

WAYS OUT
  → <a href="the_corridor.md">The corridor</a>                      Marek here 00:20–01:30
  → <a href="the_office.md">The office</a>            🔒 "the door's shut and the light's off"   unless Del is up
  → <a href="the_lot.md">The lot</a>
  → <a href="the_kitchen.md">The kitchen</a>
  → <a href="the_bathroom.md">The bathroom</a>
</pre>

---

## Why each thing is here

**Take the check-in** is the money and the exhibitionism surface at once — a stranger at the counter,
looking at her, several times a night. It is the only choice on this screen that is *not* always
available, and that is correct: it appears when a car has arrived.

**Watch the monitor** is the corruption on-ramp. Free, safe, needs nothing. ⚠️ **Day-capped, and it
has to be** — it is exactly the thing a player would click twenty times, and grinding is the genre's
second-largest complaint after lostness. Mechanism: a `_today` flag on the choice, cleared in
`[engine.daily_tick]`.

**Run the audit** is where the $80 becomes visible in Del's handwriting, which is why this game
needs no invented rent screen.

**Walk the property** is the way off the desk — and the way past twelve doors.

**Make coffee** is the cheap `energy` top-up, and the reason the kitchen is not the only answer to
being tired.

## The one change this sheet forced

**The camera monitor moved from the office to the desk.**

It was in Del's office in the decisions. But the office is locked unless Del is up — about one night
in three — and the monitor is the corruption on-ramp that has to be available from the first screen.
Gating the on-ramp behind a door that is shut two nights in three would have made the early game a
wait.

It is also just true: the clerk watches the cameras. That is the job. Del has the recorder in the
office.

## Five exits — decided

Every other room has one or two; this has five, because it is the hub and everything hangs off it.

**Kept at five — LO's call, 2026-08-31.** The alternative on the table was moving the kitchen and
bathroom behind the corridor so the desk showed three, putting back-of-house one step deeper. Not
taken. Recorded so it is not re-proposed.

⚠️ **Watch it in play.** Five doors is the first thing a new player meets after the opening. If it
reads wide, the cut above is the one to make.
