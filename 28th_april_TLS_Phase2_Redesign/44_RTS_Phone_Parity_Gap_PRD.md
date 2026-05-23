# Doc 44 — RTS Phone Parity Gap PRD (what's needed for 100% alignment)

**Date:** 2026-05-21
**Builds on:** doc 42 (RTS phone, the target) + doc 43 (engine phone, as-built). 
**Status:** SCOPING ONLY — no engine code in this doc. This enumerates every gap between our built-in phone (doc 43) and RTS's phone (doc 42), and the concrete work to close each.

> **Honest framing.** RTS's "phone" is really **8 service-backed subsystems** (chat, Instafame, Naked Life, Fast Jobs, PornCenter, Bank, xCam, Quests) plus a day-tick dispatch bus and a quest engine. Literal 100% parity ≈ rebuilding all of that in our generator. Our engine already covers the **chat spine** well; the gaps are mostly the *other apps and the systems behind them*. Items below are sized (Small/Medium/Large) and phased so this is actionable, but **all of G1–G12 are required for literal 100%.**

---

## 1. Already aligned (no work)

Verified in doc 43. These RTS behaviors already work in our engine today:

- Device shell: sidebar button → modal app launcher, in-place screen swaps, unread badge.
- **Chat**: branching multi-round threads; reply choices apply trait `effects` + `flagEffects` (`sendPhoneReply` v2.py:1603) — equivalent to RTS's `InvitationMessage` + `messageStates`/`StartQuest`-via-flag pattern.
- **Condition-gated delivery**: `checkPhoneConversations` on every passage render (v2.py:1498/12810) — equal or better than RTS's once-per-day dispatch.
- **Daily repeatable chat**: `daily_topics`, 1/NPC/day with day-key reset + conditions + effects (v2.py:1880) — matches RTS's daily quick-actions cadence.
- **Dating**: swipe + `match_condition` (v2.py:2089).
- **UnlockLocation equivalent**: a reply sets a flag → a location's `entry_conditions` checks it (two-step; functionally equal to RTS `UnlockLocation`).
- **Corruption-threshold gating**: any action can gate on a raw `corruption` trait threshold.

---

## 2. Gaps → work items

Each item: *what RTS does* → *what's missing here* → *the change* → *size*.

### G1 — Delivery notification ("ding") · Small
RTS fires `createNotification("You have a new message…")` when a thread is pushed (doc 42 §5). Ours bumps the badge silently (doc 43 §5).
**Change:** in `checkPhoneConversations` (v2.py:1498), when a conversation/post transitions to newly-triggered, queue a toast via the existing `showEffectNotification`/notification path (v2.py:4771). One emission site; no schema change.

### G2 — Player social posting + follower grind · Medium
RTS Instafame: post selfie/lewd/nude (gated corruption ≥3/≥4) → gain followers (5–20/30–50/60–80) → DMs unlock at follower milestones (doc 42 §6.1). Our `social_feed` is read-only (doc 43 §7).
**Change:** add a *post* action to the `social_feed` app — buttons gated by a corruption threshold, a daily cap (day-key idiom), incrementing a `followers` core_trait. **Milestone DMs are then free**: author conversations whose `trigger` is `{trait: followers, gte: N}` — no new dispatch code. New: a post-action render + a followers increment; reuse trait effects + the existing trigger system.

### G3 — Photo quick-actions in chat · Medium
RTS chat has 3 global actions (send selfie/lewd/nude) with a corruption lock + per-action daily cooldown + per-NPC reply text + an image (doc 42 §4.3). Our `daily_topics` is close (1/day, conditions, effects) but is text-only and 1/NPC/day rather than per-action.
**Change:** extend `daily_topics` (or add a `photo_action` block) with: an optional `image`, a per-topic (not per-NPC) day-key cooldown, a corruption-tier lock with a 🔒 note, and a counter increment. Largely a generalization of the existing daily-topic mechanic (v2.py:1669).

### G4 — Quest system · Large *(decision point)*
RTS chat invites drive `StartQuest / UpdateQuest / CancelQuest` with a journal app (doc 42 §4.5, §5). We have flags + `story_arc` hints, **no quest object** (confirmed: no quest dataclass in `template_import.py`).
**Options:** (a) build a real quest primitive (quest object w/ progress steps + a Quests phone app + a `quest` condition type), OR (b) **formally adopt flags + `story_arc` nodes as the substitute** and document the pattern (cheaper; we already use flags for exactly this). Recommend (b) unless a visible quest journal is a hard requirement.

### G5 — Scheduled / delayed events · Medium
RTS `ScheduleQuest X 15` re-fires an invite in 15 days (doc 42 §4.5). **No delay queue exists** (confirmed: no `delayDays` in schema or runtime).
**Change:** add a per-event `delayDays` countdown decremented in `advanceDay` (v2.py daily-tick loop ~4437); when it hits 0, set a flag / trigger a conversation. New small state field + one day-tick loop.

### G6 — Conditional `daily_tick` effects · Small–Medium
RTS dispatch is condition-gated; our `[engine.daily_tick]` fires all flag/trait effects **unconditionally** (v2.py:4437). Today the workaround is the dual-choice mutex.
**Change:** allow an optional `conditions` block per `daily_tick` effect; wrap the apply in `triggerConditionsSatisfied`. Schema add in `TemplateDailyTick` + a guard in the loop. (General-purpose; helps beyond the phone.)

### G7 — Corruption tiers (0–4) · Small / optional
RTS uses `getCorruptionLevel() 0–4`; we use raw points (doc 43, agents confirmed). Functionally, raw-threshold conditions already cover gating.
**Change (optional):** add a derived `corruption_level` + a `corruption_level` condition operator for authoring convenience, OR just document the raw-threshold equivalence and skip. Recommend skip unless authors want tiers.

### G8 — Gallery app · Medium
RTS-style unlock-gated media gallery. Our `gallery` app is a "Coming Soon" placeholder (doc 43 §3, v2.py:2125).
**Change:** implement a `_renderGallery` that shows condition-unlocked images (reuse the trigger-stamping pattern from posts).

### G9 — Economy apps: Fast Jobs + Bank · Large
RTS Fast Jobs (4 jobs: time-of-day window + XP ladder + 2-day cooldown + payout) and Bank (1% daily interest, deposit/withdraw) (doc 42 §6.3, §6.5). No job/bank primitives exist.
**Change:** these are arguably **world systems, not phone features** — Fast Jobs can be approximated today with canvases (time-windowed via schedules) + counters (XP) + a money trait + cooldown flags; Bank interest needs a daily_tick effect (G6) + deposit/withdraw UI. A first-class "jobs app" / "bank app" would be new render + new schema. Recommend approximating with existing primitives first; promote to a dedicated app only if needed.

### G10 — PornCenter / xCam · Medium–Large
RTS PornCenter (genre × corruption-points browser; **disabled even in RTS**) and xCam (webcam: corruption ≥4 + a `webcam` item) (doc 42 §6.4, §6.6, §G). 
**Change:** PornCenter ≈ the Gallery app (G8) gated by corruption tiers. xCam ≈ a `custom` app (G12) + a content scene. Low priority (PornCenter is dormant in RTS itself).

### G11 — In-world phone purchase · Small
RTS buys the phone for $400 (`isPurchased('phone')`) (doc 42 §2). Ours is on/off via metadata (doc 43 §1).
**Change:** gate the sidebar `phoneButton` render (v2.py:13520) on a flag or owned-item instead of (or in addition to) the metadata switch, so the phone can be acquired in-world. Small condition guard.

### G12 — `custom` app type · Medium
RTS has bespoke app screens (Naked Life forum, Statistics). Our `custom` app is a placeholder (doc 43 §3).
**Change:** implement `custom` as an author-defined screen that renders a named canvas/passage inside the phone frame, so arbitrary mini-apps (rank board, stats, xCam) can be authored without per-app code.

---

## 3. Recommended phasing

Literal 100% needs **all of G1–G12**. If pursued incrementally:

- **Tier 1 — make the chat *feel* like RTS** (highest value / lowest cost): **G1** (ding), **G6** (conditional daily-tick), **G3** (photo quick-actions). Mostly extends existing systems.
- **Tier 2 — the social + story spine:** **G2** (posting + followers + milestone DMs), **G5** (delayed events), **G4** (quest decision — adopt flags+story_arc or build the primitive).
- **Tier 3 — the remaining apps:** **G8** (gallery), **G12** (custom app), **G11** (in-world purchase), **G7** (corruption tiers, optional), **G9** (jobs/bank), **G10** (PornCenter/xCam).

**Effort reality:** Tier 1 is days; Tier 2 is the bulk of the "RTS phone feel"; Tier 3 (esp. G9) is where literal parity becomes a large build. Most TLS value lives in Tiers 1–2 — the chat-and-social spine — because that's what the engine is already 80% of the way toward.

---

## 4. The two true blockers (everything else extends existing primitives)

1. **Delay queue (G5)** — nothing today can "fire in N days." Genuinely new.
2. **A quest object (G4)** — *if* a visible quest journal with progress steps is required; otherwise flags + `story_arc` already substitute.

Every other gap (G1, G2, G3, G6, G8, G11, G12) is a generalization of an existing mechanism (notifications, trigger conditions, daily-topic cadence, trait counters, app renderers). G9/G10 are large but are world/economy systems more than phone features.

---

*Companions: doc 42 (RTS phone target), doc 43 (engine phone as-built). Engine anchors: `apps/game_generation/twee_comprehensive/generators/v2.py` (1498 delivery, 1603 reply effects, 1669 daily chat, 1960 feed, 2012 dating, 2125 placeholder, 4437 daily_tick, 4771 notifications, 13520 sidebar button); `apps/projects/services/template_import.py:173–252, 1593–1696` (schema/parser).*
