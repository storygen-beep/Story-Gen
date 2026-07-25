Title: Vesper
Subtitle: The Official Guide
Version: 0.1.5
Release: 2026-07-25
Cover: ../output/videos/portraits/wren_cover.jpg
Byline: Written by the developer. Distributed to patrons.

# About This Guide

This guide covers **Vesper v0.1.5**. It assumes nothing about how far you've
gotten and it does not hold anything back.

!!! spoiler "Read at your own risk"
    Every gate, threshold and consequence in the current build is printed here,
    including the ones the game works hard to make you discover. If you would
    rather find them yourself, close this now and come back when you're stuck.

## What this guide does

Three things, and nothing else:

1. **Tells you the recommended action** — where to be, who to be near, what to wear.
2. **Shows you how she reacts** — the exact number a choice moves, and what that number opens.
3. **Warns you about consequences** — the choices that cost you a route, and the states that lock you out of a room.

If a line in this guide isn't one of those three, it shouldn't be here.

## What this guide does *not* do

It doesn't retell the story. There are no scene summaries and no plot recaps —
the writing is the thing you paid for and reading it here would be worse than
playing it. Where a scene matters mechanically, it's named, not described.

It also doesn't list every choice. **If a choice isn't mentioned in this guide,
it doesn't affect progression.** That's the single most useful sentence in the
document: the game has 255 choices and roughly forty of them are load-bearing.
The rest are flavour, and you can pick whichever you like.

## Corrections

Found a wrong number or a route that doesn't work? Post it in the patron Discord
with your build version — it's in the sidebar footer, bottom-left, next to the
release date. Corrections ship in the next revision of this file.

> **Sample build.** This is a layout proof. The meter bands, the Renner
> thresholds and the Condition gate are read from the shipped v0.1.5 data and are
> correct. Anything in *The Undertow* chapter is placeholder structure, not
> verified numbers.

# How To Read Her

Everything in Vesper runs off four things: the meters in the sidebar, what
she's wearing, where she is, and what time it is. Learn these four and the rest
of the guide is a lookup table.

## The meters

Three read-outs sit in the sidebar. Two are always there. The third only appears
once the game has done something to her.

| Read-out | Range | What it means |
|---|---|---|
| **Charge: Critical** | `0–24` | She's running out. Most activities are closed to you. |
| **Charge: Low** | `25–49` | Enough for one job, not two. |
| **Charge: Steady** | `50–74` | The working band. Live here. |
| **Charge: Full** | `75–100` | Topped off. Nothing is gated above this — no reason to hoard. |

Charge is her energy. It's spent by work and by travel, and it comes back when
she's used — sex charges her. That inversion is the whole economy of the game:
the thing that costs a person is the thing that feeds her.

| Read-out | Range | What it means |
|---|---|---|
| **Condition: Filthy** | `0–39` | **You cannot go out in cover.** Wash first. |
| **Condition: Used** | `40–74` | Fine for the tower and the Waterfront. |
| **Condition: Clean** | `75–100` | Fine everywhere. |

!!! warning "The one gate that will strand you"
    Condition below 40 blocks travel to the Reach. If you've just come off a
    scene and the trip isn't offered, this is why. Wash in her room, then go.
    Nothing else in the build hides an exit this quietly.

The third read-out — **Core** — does not exist for most of the game. It appears
the first time she's used after captivity and it never goes down. Each use pushes
it a full step. Once it reads **Core: Failing** it stays there permanently; it is
not a resource you manage, it's a clock you watch. The repair route is the only
thing in the game that touches it.

## Cover

Out of cover, she's a stranger. Nobody outside the company deals with a stranger.

Cover is a **worn garment**, not a state of mind — the game re-checks what she's
actually wearing every time it matters. Put the right clothes on before you
travel, not after you arrive.

| Where you're going | What she wears | Where it is |
|---|---|---|
| Renner's Depot, the Anchor | Dock-work coveralls | Her room |
| Vance Securities, the Docs Department | Analyst's grays | Her room |
| The Undertow, the Underground | Whatever the underworld reads as harmless | Her room |

![Cover: the analyst](../output/videos/portraits/wren_cover_analyst.jpg)
*Analyst's grays. What the tower sees.*

# The City

Twenty-five rooms across two street hubs. **Spire Plaza** is the company side;
**the Waterfront** is everything else. You bridge them by travelling, and
travelling costs Charge and clock.

| Location | Hub | Opens when |
|---|---|---|
| Spire Plaza | — | Start |
| Vance Securities | Spire | Start |
| The Docs Department | Spire | Mission 1 active |
| The Vault | Spire | Calloway's route |
| The Atrium | Spire | Start |
| Mercer's Penthouse | Spire | Start |
| Wren's Floor / Wren's Room | Spire | Start |
| The Waterfront | — | Start |
| The Anchor | Waterfront | Start |
| Renner's Depot | Waterfront | After Renner hires her |
| The Berth | Waterfront | Kess's route |
| The Underworld Gate | Waterfront | Mission 1 complete |
| The Undertow | Underground | Through the Gate |
| The House | Underground | Through the Gate |
| The Pit, The Black Market | Underground | Through the Gate |

A locked room is still visible on the map. If you can see it and can't enter it,
the game will tell you why in one line — read the refusal, it's the hint.

# Mission 1 — Renner

Renner supplied the gear that outfitted the facility Cain burned down. He never
knew what it was for. The company wants the rogue; she wants the way in. Either
way the job is the same: get inside his life and drain him.

![Renner's route](../output/videos/portraits/wren_grays.jpg)

## Getting hired

**Wear the coveralls before you leave her room.** Out of cover he sees a
stranger and won't deal with her at all — this is the single most common place
new players stall.

Then find him at **the Anchor**. Taking the work sets `renner_hired` and opens
**Renner's Depot** on the Waterfront.

## Earning the office

Work the depot haul. Every haul pushes his **relation**.

| Goal | Threshold | What it opens |
|---|---|---|
| Earn the office | `relation ≥ 21` | He waves you into the back office |

There's no trick here and no faster route — it's repetition, and it's meant to
be. The office is where the seduction opens; nothing before it counts.

## The ladder

Once the office is open, the route is a **stepped corruption ladder**. One rung
is live at a time. The quest card swaps as his corruption climbs, so the card in
your sidebar is always the rung you're actually on.

| Rung | Live while | Push corruption to |
|---|---|---|
| **Tease** — make him look up from the manifest | `corruption < 10` | `10` |
| **Flash** — let him see there's nothing under the coveralls | `corruption 10–19` | `20` |
| **Grope** | `corruption 20–29` | `30` |

Run the rung in cover, in his office. Each rung has its own scene and each one
pushes him toward breaking.

!!! warning "Don't skip the cover check"
    The rungs re-check the coveralls every time. Coming in out of cover doesn't
    fail loudly — the rung simply isn't offered, and it reads like a bug.

When the ladder tops out, the drain closes the mission and sets
`renner_drained`. **The Underworld Gate** opens on the Waterfront.

# The Undertow

*Placeholder chapter — structure only, numbers not verified for this proof.*

Down through the Gate. The Undertow is a bar with a bartender who has outlasted
every owner it's had, and it has had a few.

| Who | Where | When |
|---|---|---|
| **Sol** — bartender | The Undertow | Always |
| **Colm** — Bastien's courier | The Undertow | Every night |
| **Rue** — madam | The House | Working hours |
| **Bastien** — the quiet owner | Never in front of anything | — |

Sol and Colm are **portrait hubs**, not location links: click the portrait in
the room, not a nav card. Colm's on-ramp gates on his own relation — first meet,
then Talk, then Drink, then the rest as the number climbs.

# Cheats

The cheat page is in the game, not in this document. It's diegetic — it doesn't
call itself a cheat menu — and it's always available once you know where it is.

It gives you **money and the climbing meters**. It does not give you story
progress: no flags, no route skips, no stage jumps. That's deliberate. It's there
so you never have to grind a number you've already proven you can move, and it
will not let you skip a scene you haven't reached.

If a meter is the only thing standing between you and the next rung, use it
without guilt. If a *flag* is what's missing, the cheat page can't help and the
route above tells you what will.

# What's In This Build

v0.1.5 is finishable end to end. The content that exists:

- The cold open and the tower
- **Mission 1 — Renner**, complete through the drain
- The underworld: the Gate, the Undertow, the House
- Captivity and the Core
- The Reach and the repair route
- The Archive — infiltration through the handoff

Not yet in: the crack payoff, and the income apex. Both are next.

Thanks for reading, and for funding it.
