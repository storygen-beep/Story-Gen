# OPENING — the screen walk  `[READY]`

The only view a design cannot satisfy by intent: **a screen either exists or it does not.**

**Shape: COLD OPEN.** F1's two shapes are separated by **who is named**, not by length. This one
names **nobody**. Wren's situation and the pressure, and no people at all. All seven arrive later,
each through their own meeting.

⚠️ **The defect is the middle** — a cold open carrying a staged open's payload. Our own measured
failure named **six people, two of whom are not in the game at all**, and put none of them on
screen. The rule is consistency: the cast load and the word budget have to agree.

---

## The walk

<pre>
  #  canvas · node              what is on the screen                        the button
 ────────────────────────────────────────────────────────────────────────────────────────────────
  0  Start          <b>ENGINE</b>      title card · age gate                        "✓ I am 18 or older - Enter Game"
  1  CustomizeCharacters         <b>DELIBERATE ABSENCE — see below</b>                 —
 ────────────────────────────────────────────────────────────────────────────────────────────────
  2  open_boot · <i>boot</i>            what she is, who holds the leash, and     "Somebody has to pay for the night."
                                 that the charge is going down. NO NAMES.
  3  open_boot · <i>past</i>            the start choice — what she was before    "Hands. Weather. Other people's cargo."
                                 the company took her                       "Somebody paid for me before they did."
                                                                            "I have stood on a floor like this."
     ── location exit ──►  <b>kess_berth</b>, 10:33 · sets <b>one</b> of past_field / past_house / past_floor
 ────────────────────────────────────────────────────────────────────────────────────────────────
     <b>THE FUNNEL ENDS.</b>  Live at kess_berth, 10:33: the feed line (10 coin), the bench,
     Kess himself (10:00-22:00), and the engine's own Change Clothes link.
</pre>

⚠️ **Rows 0 and 1 go in even though we do not author them.** Leaving them off is how a sheet ends up
describing an opening the player never has. **The player's first screen is never beat 1.**

⚠️ **Every button above is quoted, not summarised.** *"The player continues"* is not a row. Three of
the four are written; none is `Continue`.

## Screen 1 — the deliberate absence

`CustomizeCharacters` exists only when `customizable = true` with a declared
`[[player.customization_fields]]` entry, and declaring one **repoints the age gate at it**
(`v2.py:1065`, `:9251`). Its headings and button are hard-coded — *"Customize Characters"*,
*"Personalize the characters in your story"*, *"Continue to Game"* — in a product voice, as the
second thing a player reads. **Seven of fifteen built games ship it.**

The Want declines a creation step: Wren is `written`, and what a blank slate buys is bought instead
by the start choice on screen 3. So this row is an **absence on purpose**, recorded rather than
omitted.

⚠️ Gate `what she picks is read` will report **n/a** for this game. `n/a` is **not a pass** — it is
an absence, and this paragraph is the reason it is one.

## Screen 2 — the boot

`[INTENT]` ~150 words, one node, one screen. It carries three things and no fourth:

1. **What she is** — a Vance Dynamics asset, and what that means about her body rather than her job.
2. **Who holds the leash** — *the company*, never a name. F7's ordering with the name withheld
   entirely: the player gets the role now and every name later, when it is earned.
3. **The pressure** — the charge is going down and the night costs ten. This is the obligation
   arriving before any character does, which is `the-economy.md` R3's *"armed after income exists"*
   read forward: she is told the price on screen two and shown the earner on screen four.

**No character is named anywhere on this screen.** That is the cold open, and it is checkable by
reading this sheet against the cast list.

## Screen 3 — the start choice

**A memory, not a slider.** Asked in the scene that is already asking it: the company's line is that
she has never been anything else, and the boot has just said so. Three buttons, one flag each, no
stat screen and no numbers.

| button | flag | read at |
|---|---|---|
| "Hands. Weather. Other people's cargo." | `past_field` | `renner_depot` · `underworld_bar` · `the_street` · `kess_berth` |
| "Somebody paid for me before they did." | `past_house` | `penthouse` · `mercer_room` · `underworld_brothel` · `kess_berth` |
| "I have stood on a floor like this." | `past_floor` | `underworld_bar` · `underworld_strip` · `underworld_brothel` · `bastien_backroom` |

Four to five read sites each, as a **band on a standing surface** — the answer changes what a room
says, never what it allows. `mrs_vance` is the worked shape: three inert choices became three flags
read at five sites each.

⚠️ **THE PLACEMENT TRAP.** Adjacent `[group]` blocks merge into ONE if/elseif chain
(`v2.py:14637`) and first match wins. A past-band dropped beside a surface's existing ladder makes
**that ladder unreachable for every player carrying a past** — no error, no build warning, the prose
simply stops appearing. Separate the two chains with any non-`group` block. Both surfaces this was
first built on already had a ladder.

## F3 — the handover, computed

The gate computes this exactly, so the sheet does too:

```
[time] starting_hour = 10                                    10:00
  open_boot · boot renders                                   10:00
  → past          no time declared → default 3 min           10:03    v2.py:13200
  → location exit  time_progression_minutes = 30             10:33
```

**Landing: `kess_berth` at 10:33.** Kess's schedule row is `Mon-Sun 10:00–22:00`. **10:33 is inside
it**, so the room has a scheduled body, a need she can fill, and a priced door on the first free
screen.

⚠️ **A random ambient would not count** (`trigger_mode = "random"` is a coin flip) and **neither
would a walk-in** (`substitution_only = true` has no door of its own). The measured failure landed a
player at 07:36 in a room whose three work canvases opened at 08:00, 13:00 and 21:00 — *the player's
first free act in that game is pressing a wait button.*

## F4 — every live system, and where it is taught

> *"A system the player never sees taught is a system you might as well not have wired."*

Either a named beat in the first hour arms it, **or it sits on the sidebar at value-zero where the
player can read it.** The sidebar half is permanent, and a banded stat reading near-empty against
its ceiling **is** the "there is a climb ahead" read on frame one, with no teach screen.

| system | where it is taught |
|---|---|
| `charge` | screen 2 names it going down; screen 4 sells the fix at 10 coin |
| `coin` | screen 2 names the price; the sidebar carries the number |
| `seated` | the bench is on the landing screen; armed at Kess's arc step 3 |
| `cover` | sidebar at value-zero, and the engine's own `Change Clothes` link at the berth |
| `clean` | sidebar at value-zero; first shut door teaches it |
| `service` · `drain` | sidebar, banded, at value-zero — the climb-ahead read |
| `arousal` | **not surfaced in the opening.** It gates the act menu and nothing else, and there is no act menu in the first hour. |

⚠️ **`wardrobe_location` puts its own door on the screen** (`v2.py:9814`), unconditionally, above
the portrait row. Do not author a second one — `orientation` did, and the authored one is the one
that did not work.

## What is live on the screen it hands over to

`kess_berth`, 10:33 — three rows and the engine's link:

- **"A night on the line. (10 coin.)"** — the obligation and the only `charge` fill point
- **"Hold still."** — the bench, once `kess_tenant` is set
- **Kess** — portrait, 10:00–22:00, behind his meeting
- **Change Clothes** — the engine's, free

⚠️ **She cannot afford the night at 10:33.** That is the design: the first thing the game does is
name a price she has not got, and the second is point her at the floor that pays. It is
`the-economy.md` R3's date-and-face arriving on screen four rather than in a tutorial.
