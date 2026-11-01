# [READY] Release 1 system 1 — rent that bites

> Signed by LO: LO, 2026-11-01 ("Signed."). Step 4 of the release-1 redesign (DECISIONS 99–101), system 1 of 4.
> Changes the signed `sheets/systems/money_pressure.md` (2026-10-08); on LO's sign that sheet is rewritten to
> match and re-signed. Scope: `sheets/RELEASE1_SCOPE.md` (Mark's paid route cut, so goal 1 has no body route).

## Why it changes
- **No pressure today.** Rent is $75 (`toml_phases/0_systems_spec.toml:41`). The café pays $12–24 for a
  three-hour shift (`iterations/002/build_scripts/cafe.py:67-72`), up to three shifts a day, Monday to Saturday
  (`cafe.py:22-23`, `cafe_shift_3_today`). LO's live week paid $208. Nothing in the game costs money except
  three clothes at $20–30 (`0_systems_spec.toml:438-455`).
- **The card doesn't say it.** Week one's card reads "Week one. Class, a job, and seventy-five for Mark by
  Sunday." with the goal "Have $75 by Sunday" (`0_systems_spec.toml:494-500`). LO: it should say she pays her
  first rent to Mark this Sunday.
- **A short week costs almost nothing.** `on_short = "carry"` adds what's left to next week
  (`apps/.../generators/v2.py:14995-15011`). Vance knocks the evening after and `rent_carried` clears
  (`vance_knock`). There's no other cost.
- **LO (2026-10-31): "I say we miss first few rents inspire her to earn more."** The early weeks are built
  to come up short, so she learns that money is the problem and goes looking for more of it.
- **Paying her own way is now the only goal-1 route** (Mark's chair is cut). So it has to be hard and real.

## The design

### 1. The pay is smaller, and Tom says it
- **A shift pays $8**, which is what Tom already says ("Eight a shift, plus tips", `tom.py:41`). Tips come on
  top, set by the café customers system (system 3): a quiet shift tips $2–4, and more as the customers go
  further and she lets them.
- **One shift a day on weekdays, two on Saturday.** College takes her mornings, and the energy cost stays.
- **The sexy uniform pays in tips, not wages.** Wages are $8 in any uniform (Tom stays strict). It's the
  customers who tip more for it.

### 2. Week one is built to come up short
- She starts with **$0** (as now).
- Earliest hire: Monday afternoon, after class. First shift: Tuesday.
- **Week one at most:** five shifts × ($8 + about $3 in tips) ≈ **$55**, against **$75**. She is short by
  about $20 even if she works every day she can.
- **Week two:** $75 plus the $20 carried = $95 due. With the first customer level unlocked, a hard week makes
  about $80–100. She is close: short, or just made it.
- **Week three:** the uniform and the next customer level make **$120–160**. She can pay it all and clear the
  debt. That's when the four-Sunday streak can start.
- So a normal player misses **two rents**, and a player who grinds every shift misses one.

### 3. Missing rent costs her something she feels
Every short Sunday, in order (each is a scene that happens once, behind a flag the engine already sets):

| short Sunday | what it costs her | what changes after |
|---|---|---|
| **1st** | Mark: "Then it's owed. Vance doesn't wait, so I don't." He **takes the key to her bedroom door** until she's paid up. | `her_door_unlocked`: the house's walk-ins can now open her door (Ryan, Mark), until she clears the debt. Mark's Power +5. |
| **2nd** | Vance knocks (built, `vance_knock`). Now he adds **a $15 late fee** and says so to her face. | the fee is added to what's owed; Vance's Power +10 (built). Mark's Power +5. |
| **3rd and on** | Mark takes **one thing she bought** (the skirt, the sheer blouse, the sports bra) and keeps it in the garage until she's paid up. | the item is locked in her wardrobe; "On the table, then you get it back." Mark's Power +5 each time. |

- Paying the whole debt gives back what she lost: the key, then the item. The streak starts from that Sunday.
- **No sex for money.** Mark's prices and paid looks are cut (scope). What a short week buys is pressure,
  not an offer.
- **Ryan's cover** (built, $25 once at Love 40) stays, and still doesn't count for the streak.
- **Vance's "Come and see me"** (built, `vance_knock`) stays a hook for later. At Power 60 he asks for her;
  that answer is not in release 1.

### 4. Money has somewhere to go
- **The clothes she wants raise her tips.** The skirt ($30), the sheer blouse ($20) and the sports bra ($25)
  make a real choice: rent now, or the skirt that tips better, later.
- No other sinks in release 1.

### 5. The cards say it
- **Week one:** "Pay your first rent to Mark this Sunday: $75." Goals: go to your first class; get a job at
  the café; "Have $75 for Mark by Sunday".
- **After a short Sunday:** "You owe Mark $<owed>. He has your door key." The goal is the full sum by Sunday.
- **Goal 1** stays as built: four Sundays in a row paid in full from her own money. The tip loses "so does
  taking his chair" (the chair is cut).

## Against the taste columns
This is a system, so it runs on the four columns that fit it:
- **what she risks:** her door lock, her things, Vance at the door.
- **who sees or knows:** Mark at the table every Sunday; Vance; Ryan, who notices her door won't lock.
- **his move:** Mark takes the key and the clothes; Vance comes to her.
- **what changes after:** the open door, a locked wardrobe item, the late fee, Mark's Power.

## Engine and build work (for after the sign)
- New per-shift pay: `money(8)` plus the tip amount from system 3 (`cafe.py`).
- Shift caps: one on weekdays, two on Saturday (the `cafe_shift_<k>_today` flags exist).
- The 1st, 2nd and 3rd-short scenes: three one-time canvases on Sunday morning, read from a short-week
  counter. **Check before building:** whether the engine counts short Sundays, or a canvas has to add 1 to a
  trait on each short Sunday.
- `her_door_unlocked`: a flag the home walk-in events read (the content comes in step 5, with Ryan's and
  Mark's sheets).
- Locking one bought item while she owes: **check before building** whether the wardrobe can hide an owned
  item behind a flag.
- The week-one card text and the after-short card.
- Cut the $20 sources that belong to Mark's cut route (`mark.py:229, 292, 421, 431, 492`; `home.py:503`). Read
  each first: Laura's grocery $20 (`laura.py:453`) is an errand and stays.

## Not decided here
- Exact tip sizes: system 3, the café customers.
- Whether the rent rises ($90 after $300 paid, $100 after $900) stay as built. Proposed: yes.
