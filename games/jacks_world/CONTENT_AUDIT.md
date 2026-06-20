# Content Audit: Jack's World — Flag & Content Alignment

**Date:** 2026-02-14 (updated 2026-02-15)
**Status:** All issues fixed (A, B, C, D, E).

---

## Current Flag Progression

```
(no flags)
    ↓
kiss_unlocked              ← towel_encounter (love ≥ 10, trust ≥ 18)
makeout_unlocked
    ↓
groping_unlocked           ← bedroom_encounter (love ≥ 25, trust ≥ 22, 2+ days)
oral_unlocked                 (oral content shown in first_touch node)
manual_unlocked
    ↓
sex_unlocked               ← bedroom_moment (love ≥ 30, trust ≥ 25, 2+ days)
                              (narrative-only — deliberate penetration milestone)
```

---

## Issue A: Content Exceeds Flag Gate — FIXED

All gates updated so the required flag matches actual content level. Changes applied to both `3_activities.toml` and `6_final_game.toml`.

| # | Canvas | Node | Old Gate | New Gate | Content |
|---|--------|------|----------|----------|---------|
| 1 | Breakfast | foreplay | groping_unlocked, ≥62 | **oral_unlocked**, ≥62 | Oral stimulation |
| 2 | Movie Night | foreplay | kiss_unlocked, ≥42 | **groping_unlocked**, ≥42 | Handjob + kissing |
| 3 | Movie Night | passionate | groping_unlocked, ≥62 | **oral_unlocked**, ≥62 | Oral sex |
| 4 | Movie Night | intense | oral_unlocked, ≥82 | **sex_unlocked**, **≥65** | Full sex, anal |
| 5 | Couch Play | passionate | groping_unlocked, ≥62 | **sex_unlocked**, **≥70** | Penetrative sex |
| 6 | Couch Play | intimate | oral_unlocked, ≥82 | **groping_unlocked**, **≥62** | Manual touching |
| 7 | Morning Peek | exploration | groping_unlocked, ≥40 | **oral_unlocked**, ≥40 | Masturbation |
| 8 | Morning Peek | private | oral_unlocked, ≥55 | oral_unlocked, **≥82** | Full masturbation |
| 9 | Bedroom Play | oral | groping_unlocked, ≥72 | **oral_unlocked**, ≥72 | Blowjob |

**Tier ladders after fix:**
- **Movie Night:** start → foreplay (groping, 42) → passionate (oral, 62) → intense (sex, 65)
- **Couch Play:** start → intimate (groping, 62) → passionate (sex, 70) *(swapped order)*
- **Morning Peek:** start → exploration (oral, 40) → private (oral, 82)
- **Breakfast:** start → foreplay (oral, 62)
- **Bedroom Play:** start → oral (oral, 72)

### Canvases With No Issues

- `activity_bath_peek_angela` — self-care escalation matches gates
- `activity_morning_together_angela` — sex/intense nodes fixed to `sex_unlocked` (was `oral_unlocked`)
- `activity_deep_conversation_angela` — text only
- `activity_date_night_hotel_angela` — high gate (love≥80, trust≥30, $300), linear full arc
- `activity_spa_massage_angela` — high gate (love≥70, trust≥28), linear escalation
- `activity_bath_together_angela` — high gate (love≥70, trust≥28), linear
- `activity_exploring_kink_angela` — highest gate (love≥90, trust≥30)

---

## Issue B: Flag Progression Gap — FIXED

Flags redistributed across milestones:

| Milestone | Before | After |
|-----------|--------|-------|
| bedroom_encounter | groping, makeout | groping, makeout, **oral**, **manual** |
| bedroom_moment | oral, manual, sex | **sex only** |

`oral_unlocked` now set by `bedroom_encounter` (which shows oral content in clips 011/012). `sex_unlocked` set by `bedroom_moment` (narrative penetration milestone). The flag ladder now has meaningful separation between oral and penetration tiers.

---

## Issue C: Story Canvas Flag Mismatch — FIXED

### bedroom_encounter — now sets oral_unlocked

The `first_touch` node shows explicit oral content (clips 011, 012). Previously only set `groping_unlocked`. Now also sets `oral_unlocked` and `manual_unlocked`, matching the content shown.

**Note:** The `deep_connection` path (love≥30) still shows penetration content, but `sex_unlocked` is intentionally set at `bedroom_moment` — the deliberate relationship milestone where Angela invites penetration as an ongoing part of their life together.

### bedroom_moment — now only sets sex_unlocked

Previously set oral+manual+sex but showed no video. Now only sets `sex_unlocked`, matching the narrative description of deliberate penetration.

---

## Issue D: Choice Text Too Intense for Relationship Stage — FIXED

Changed `"Embrace her from behind"` → `"Stand closer to her"` in Breakfast canvas. Subtle intent at love 22, lets the scene (embrace at counter) unfold organically from the video rather than being player-directed.

---

## Issue E: Inconsistent Love Thresholds — FIXED (via Issue A #8)

Morning Peek `private` node threshold raised from love≥55 to love≥82, matching all other canvases.

---

## Issue F: Sex-Tier Pacing Gap — FIXED

After fixing Issues A–E, verification found a 49-point gap between `sex_unlocked` (love ~33 via `bedroom_moment`) and the first sex activity (love 82). Lowered two thresholds to place first sex content in the "intimate" emotion range (love 61–80):

| Canvas | Node | Old Threshold | New Threshold |
|--------|------|--------------|---------------|
| Movie Night | intense | love ≥ 82 | **love ≥ 65** |
| Couch Play | passionate | love ≥ 82 | **love ≥ 70** |

Gap narrowed from 49 to 32 points. Higher-tier activities (Date Night, Exploring Kink, Spa, Morning Together, etc.) remain at love ≥ 82 as premium content.

---

## Issue G: Morning Together Wrong Flag — FIXED

Verification found `activity_morning_together_angela` sex and intense nodes gated by `oral_unlocked` despite showing penetrative content. Changed to `sex_unlocked`:

| Node | Love | Old Flag | New Flag | Content |
|------|------|----------|----------|---------|
| sex | ≥ 82 | oral_unlocked | **sex_unlocked** | Full penetration |
| intense | ≥ 92 | oral_unlocked | **sex_unlocked** | Penetration + anal |

---

## Content Rule (Proposed)

Each flag should define a maximum content level. No node should show content above what its required flag permits:

| Flag Gate | Max Content Allowed |
|-----------|-------------------|
| No flags | Proximity, eye contact, domestic moments |
| kiss_unlocked | Kissing, hand-holding, leaning close |
| groping_unlocked | Touching, caressing, undressing, handjobs |
| oral_unlocked | Oral sex, mutual manual stimulation |
| sex_unlocked | Penetration, full sex, anal |

---

## Summary: All Issues

| # | Type | Canvas | Node | Description | Status |
|---|------|--------|------|-------------|--------|
| 1 | Content > Gate | Breakfast | foreplay | Oral content behind groping gate | FIXED |
| 2 | Content > Gate | Movie Night | foreplay | Handjob behind kiss gate | FIXED |
| 3 | Content > Gate | Movie Night | passionate | Oral behind groping gate | FIXED |
| 4 | No gate exists | Movie Night | intense | Penetration behind oral gate (no sex_unlocked gate) | FIXED |
| 5 | Content > Gate | Couch Play | passionate | Penetration behind groping gate | FIXED |
| 6 | Undercontent | Couch Play | intimate | Manual touching behind oral gate | FIXED |
| 7 | Content > Gate | Morning Peek | exploration | Masturbation behind groping gate | FIXED |
| 8 | Threshold | Morning Peek | private | love≥55 vs ≥82 standard | FIXED |
| 9 | Content > Gate | Bedroom Play | oral | Blowjob behind groping gate | FIXED |
| 10 | Choice text | Breakfast | warm | "Embrace from behind" too intense at love 22 | FIXED |
| 11 | Flag mismatch | bedroom_encounter | deep_connection | Shows penetration, only sets groping_unlocked | FIXED |
| 12 | Flag mismatch | bedroom_moment | all | Sets oral+sex_unlocked but shows no video | FIXED |
| 13 | Flag bundling | bedroom_moment | — | oral_unlocked and sex_unlocked set simultaneously | FIXED |
