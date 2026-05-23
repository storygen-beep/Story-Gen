# Doc 45 — Engine PRD: 100% RTS Phone Parity

**Date:** 2026-05-22
**Builds on:** doc 42 (RTS phone target), doc 43 (engine phone as-built), doc 44 (gap spec G1–G12). Executable engineering PRD in the lineage of doc 25 (Lane 3) / doc 37 (clothing).
**Status:** Tier 1 (G1 + G6 + G3) ✅ **SHIPPED 2026-05-22** (schema+parser+serialization in `template_import.py`; runtime in v2.py **and** v1.py; `[phone]` + new fields documented in `COMPREHENSIVE_SYSTEM_REFERENCE.md`; tests in `apps/projects/tests.py` — `DailyTickConditionsSchemaTests`, `PhoneParityFieldsSchemaTests`, `PhoneParityIntegrationTests` v1+v2; 283 projects-suite passed, 0 new failures; TLS + under_one_roof builds clean; twee inspection + browser live-play GREEN — G1 toast fires, G3 thread renders, G6 guard emitted). **Tier 2 (G4 + G5 + G2) ✅ SHIPPED 2026-05-22** — real quest primitive (`[[quests]]` + `questEffects` on canvas+chat choices + `quest` condition + Quests app + `applyQuestEffect`), delay queue (`scheduleEffects` + `$game_state.scheduled` decremented in advanceDay + `scheduleEvent`/`fireScheduledEvent`), player social posting (`social_feed` `post_actions`: corruption-gated + daily-capped + `followers` counter via `sendSocialPost`). Both v1+v2; `[[quests]]`/questEffects/quest-condition/scheduleEffects/post_actions documented in SYSTEM_REFERENCE; tests `QuestSchemaTests`/`PhonePostActionsSchemaTests`/`Tier2RuntimeIntegrationTests`(v1+v2). 288 projects-suite passed (0 new fails; same 5 pre-existing game_generation fails). TLS + under_one_roof builds clean; twee inspection + browser live-play GREEN (quest start/step/complete, schedule fires, post→+followers, daily-cap blocks 2nd). **Tier 3 (G7 + G8 + G11 + G12 + G10 + G9) ✅ SHIPPED 2026-05-22 → doc 45 100% PARITY COMPLETE.**
- **G7** corruption tiers: `getCorruptionLevel()` (thresholds [0,5,15,30,45], `[engine].corruption_tiers` override) + `corruption_level` condition.
- **G8** gallery app: `[[phone.gallery_items]]` (image/caption/trigger/link) + `_renderGallery` (trigger-gated, clickable `link`→`Engine.play`).
- **G11** in-world purchase: `[phone].purchase_flag` gates the sidebar `phoneButton` widget.
- **G12** custom app: app `passage` → `_renderCustom` wikis the passage in-frame.
- **G10** PornCenter/xCam: documented authoring recipe over G7+G8+G12+G11 (no new engine).
- **G9** economy: `[[fast_jobs]]` + fast_jobs app (`doFastJob`: income+xp+cooldown, cooldowns decremented daily); `[bank]` + bank app (deposit/withdraw + daily interest in advanceDay).
Both v1+v2; all fields documented in SYSTEM_REFERENCE incl. the G10 recipe; tests `Tier3SchemaTests` + `Tier3RuntimeIntegrationTests`(v1+v2). 293 projects-suite passed (0 new fails; same 5 pre-existing game_generation fails). TLS + under_one_roof builds clean; twee inspection + browser live-play GREEN (level-3 tier gate, job payout+xp+cooldown-block, bank deposit). **All 12 gaps G1–G12 shipped — doc 45 closed at 100% RTS-phone parity.**
**Scope decision (user, 2026-05-22):** literal **100%** — all twelve gaps including the heavy world-systems (G9 jobs/bank, G10 PornCenter/xCam) — and a **real quest primitive** for G4 (not the flags/`story_arc` substitute).

> **Reality up front.** RTS's "phone" is 8 service-backed subsystems + a quest engine + a day-tick dispatch bus. Our engine already covers the *chat/social/dating spine* (doc 43). The two genuinely-new subsystems here are **G5 (delay queue)** and **G4 (quest primitive)**; everything else extends a mechanism that already exists (notifications, daily-topic cadence, trait counters, the condition dispatch, app renderers, `buyItem`). Tier 1 is days of work; Tier 3 (esp. G9) is multi-week.

---

## 0. Cross-cutting requirements (apply to every work item)

- **Both generators.** Every runtime change lands in `apps/game_generation/twee_comprehensive/generators/v2.py` (default) **and** mirrors to `v1.py` (parity — the phone + `daily_tick` already exist in both). Keep untouched paths byte-stable (the v2-fork regression test depends on it).
- **Schema path.** `apps/projects/services/template_import.py` — add the dataclass + parser branch + metadata serialization. Phone parser lives at `1593–1696`; `TemplateDailyTick` at `345`; reuse the effect shapes `TemplateChoiceEffect` / `TemplateFlagEffect`.
- **Tests.** `apps/projects/tests.py` — schema tests as `SimpleTestCase`, integration as `TestCase`/`TransactionTestCase` (follow `DailyTickSchemaTests`:546 and `FlagOpAndDailyTickIntegrationTests`:577, incl. the advanceDay-loop test at 696). Generator-level cases go in `apps/game_generation/tests.py`.
- **Docs.** `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` currently has **no `[phone]` section at all** — the first implemented tier must add the base phone authoring docs (from doc 43) + every new field this PRD introduces.
- **Per-item verify.** `package_from_toml` build clean (no new warnings) → `pytest` green (new tests) → twee inspection of the emitted JS/state → browser live-play (twine-game-explorer) on a phone-enabled game.
- **Back-compat.** Every new field is optional with today's behavior as the default; absent ⇒ byte-identical output.

### Verified engine anchors (every change below cites one)
| Area | Anchor |
|---|---|
| Phone runtime block | `v2.py:1494–2166` |
| Delivery scan (every passage render) | `checkPhoneConversations` `v2.py:1498`, called at `12810` |
| Chat reply effects/flags | `sendPhoneReply` `v2.py:1603` |
| Daily chat send / render | `sendDailyChat` `v2.py:1669` / render `1871` |
| Social feed / dating / placeholder | `_renderSocialFeed` `1960` / `_renderDatingApp` `2012` / `_renderPlaceholder` `2125` |
| App-type dispatch (add new apps here) | `v2.py:1743–1745` |
| Notifications | `setup.pendingEffects` + `showEffectNotification` `4772` (warning variant `notify-warning` `4813`) |
| Condition dispatch chain (add new types here) | `v2.py:2942–3133`; corruption already special-cased at `1325` |
| Effects + daily_tick loop | `applyAndNotifyTrait` `4715`; daily_tick loop `4437–4477` |
| Purchase precedent / sidebar button | clothing `buyItem` `v2.py:1344`; `phoneButton` `13520` |

---

## Tier 1 — make the chat/feed *feel* like RTS (≈ days)

### G1 — Delivery notification ("ding")
**RTS:** `createNotification("You have a new message…")` on push (doc 42 §5). **Ours:** badge bumps silently (doc 43 §5).
- **Runtime (only):** in `checkPhoneConversations` (`v2.py:1498`), when a conversation/post transitions to *newly* triggered this scan, push a phone toast onto `setup.pendingEffects` and call `setup.showEffectNotification()` (`4772`). Mirror to v1.
- **Schema (optional):** per-conversation/post `notify` string (default: `"New message"` / `"New post"`).
- **Tests:** integration — set a trigger condition true, render a passage, assert a toast was queued; badge still increments.
- **Accept:** a freshly-triggered conversation produces one toast on the next passage; already-triggered ones don't re-toast.

### G6 — Conditional `daily_tick` effects
**RTS:** dispatch is condition-gated. **Ours:** `daily_tick` fires all effects unconditionally (`v2.py:4437`).
- **Schema:** add optional `conditions` (the standard `{version, logic, items}` block) to each `TemplateDailyTick` flag- and trait-effect (`template_import.py:345`).
- **Runtime:** in both daily_tick loops (`v2.py:4437–4477`), wrap each apply in `if (!eff.conditions || setup.triggerConditionsSatisfied(eff.conditions)) { … }`. Mirror to v1.
- **Tests:** extend `DailyTickSchemaTests` (parse round-trip) + the advanceDay integration test (effect applies only when condition holds; no `conditions` ⇒ unchanged).
- **Accept:** `daily_tick` effect with `conditions` fires only when satisfied; back-compat byte-stable.

### G3 — Photo quick-actions in chat
**RTS:** global send-selfie/lewd/nude with corruption lock + per-action daily cooldown + per-NPC reply + image (doc 42 §4.3). **Ours:** `daily_topics` is text-only and capped 1/NPC/day (doc 43 §6).
- **Schema:** extend `TemplatePhoneDailyTopic` (`template_import.py:236`) with optional `image`, `corruption_min`, and a per-topic cooldown flag (so several photo actions can each be 1/day rather than 1/NPC/day).
- **Runtime:** generalize `sendDailyChat` (`v2.py:1669`) + the daily-topic render (`1871`): switch the cooldown key from per-NPC to per-topic day-key; add a 🔒 lock with note when `corruption < corruption_min`; render an image bubble; increment an author-named counter trait. Mirror to v1.
- **Tests:** schema round-trip + integration (locked under threshold, 1/topic/day, image emitted).
- **Accept:** photo action locks below `corruption_min` with a note; usable once/day/topic; image renders in the thread.

---

## Tier 2 — the social + story spine (the bulk of the RTS feel)

### G2 — Player social posting + follower grind
**RTS:** post selfie/lewd/nude (corr ≥3/≥4) → followers (5–20/30–50/60–80) → DMs unlock at milestones (doc 42 §6.1). **Ours:** `social_feed` is read-only (doc 43 §7).
- **Schema:** `social_feed` app gains `post_actions` (list of `{label, corruption_min, followers_min, followers_max, daily_cap, counter_trait}`).
- **Runtime:** in `_renderSocialFeed` (`v2.py:1960`) render post buttons gated by corruption + a day-key daily cap (reuse the `daily_chats` idiom), and on post increment the author-named `followers` core_trait via `applyAndNotifyTrait` (`4715`) by `random(min,max)`. Mirror to v1.
- **Milestone DMs come for free:** author a conversation whose `trigger` is `{type:"trait", trait_key:"followers", operator:"gte", value:N}` — no new dispatch code (delivery already condition-scans, G/doc 43 §5).
- **Tests:** schema + integration (post raises `followers`; daily cap blocks the 2nd; lewd/nude hidden under corr gate).
- **Accept:** posting grows a followers trait under a daily cap; corruption tiers gate the spicier posts; a milestone-triggered DM arrives.

### G5 — Delay queue (scheduled / delayed events)
**RTS:** `ScheduleQuest X 15` re-fires in 15 days (doc 42 §4.5). **Ours:** none.
- **Schema:** a scheduled-event entry carrying `delayDays` + an action (`start_quest` / `set_flag` / `trigger_conversation`). Surface as a `ScheduleQuest`-style effect available to chat-reply + canvas choices, and/or a top-level scheduled list.
- **Runtime:** a `$game_state.scheduled[]` queue; in `advanceDay` (the `4433` region) decrement each `delayDays`; at 0 fire the action and remove it. Mirror to v1.
- **Tests:** integration — schedule an event, advance N days, assert it fires exactly once on day N.
- **Accept:** an event scheduled for N days fires on day N and not before/again.

### G4 — Quest primitive (real)
**RTS:** `StartQuest/UpdateQuest/CancelQuest` drive a journal (doc 42 §4.5, §5). **Ours:** flags + `story_arc` hints, no quest object.
- **Schema:** `TemplateQuest` (`id`, `name`, ordered `steps`/`stages` each with a `journal_entry`, optional `repeatable`). A `[[quests]]` top-level list parsed in `template_import.py`.
- **Runtime:**
  - Quest state in `$game_state.quests` (`{active, progress, completed}` per id).
  - Macros `StartQuest` / `UpdateQuest <id> <step> <text>` / `CancelQuest` / `CompleteQuest`, emitting like the existing flag-effect path; expose as `questEffects[]` on chat-reply choices (`sendPhoneReply` `1603`) and canvas choices.
  - A **Quests app** render (new branch in app dispatch `1743–1745`) listing active/completed quests + current step (mirror the existing `Quests`-style journal styling).
  - A **`quest` condition type** added to the dispatch chain (`v2.py:2942–3133`): `{type:"quest", quest_id, operator:"active"|"completed"|"step_gte", value}`.
  - Mirror all to v1.
- **Tests:** schema round-trip + integration (start → update step → complete; `quest` condition gates a canvas; journal renders; `CancelQuest`).
- **Accept:** a quest progresses through steps, gates content via the `quest` condition, shows in the Quests app, and can be cancelled/rescheduled (with G5).

---

## Tier 3 — remaining apps + parity tail (large; esp. G9)

### G7 — Corruption tiers (0–4)
**RTS:** `getCorruptionLevel()` with `pointsMap = [0,5,15,30,45]` (doc 42 §10.1). **Ours:** raw points.
- **Schema (optional):** configurable tier thresholds (default `[0,5,15,30,45]`).
- **Runtime:** add a `corruption_level` condition type to the dispatch chain (`2942+`) computing level from points via the map; expose a `getCorruptionLevel()` helper (precedent: corruption already special-cased at `1325`). Mirror to v1.
- **Tests + Accept:** `corruption_level gte 3` is true iff points ≥ 30; raw-threshold conditions still work.

### G8 — Gallery app
**Ours:** `gallery` is a "Coming Soon" placeholder (`_renderPlaceholder` `2125`).
- **Schema:** `[[phone.gallery_items]]` (`id`, `image`, `trigger`, optional `caption`).
- **Runtime:** `_renderGallery(appId)` (replace the placeholder branch in app dispatch `1743–1745`) showing trigger-unlocked images; reuse the post trigger-stamping from `checkPhoneConversations`. Mirror to v1.
- **Accept:** an item appears in the gallery once its `trigger` holds.

### G12 — Custom app
**Ours:** `custom` is a placeholder.
- **Schema:** app gains a `passage`/`canvas` ref.
- **Runtime:** `custom` renders the referenced canvas/passage *inside* the phone frame (in-place, like the other apps). This unblocks bespoke mini-apps without per-app code. Mirror to v1.
- **Accept:** a `custom` app shows an arbitrary authored screen in-phone.

### G11 — In-world phone purchase
**RTS:** buy the phone for $400 (`isPurchased('phone')`, doc 42 §2). **Ours:** on/off via metadata.
- **Schema:** phone `purchase` block (`item`/`flag` + `price`).
- **Runtime:** gate the `phoneButton` render (`v2.py:13520`) on the flag/owned-item (in addition to `enabled`); reuse the clothing `buyItem` flow (`1344`) for the transaction. Mirror to v1.
- **Accept:** the sidebar button is hidden until the phone is acquired in-world.

### G9 — Economy apps: Fast Jobs + Bank (LARGE — flag as multi-week)
**RTS:** Fast Jobs (income + time-of-day window + XP ladder + 2-day cooldown + payout) and Bank (1% daily interest, deposit/withdraw) (doc 42 §6.3, §6.5).
- **Schema:** `TemplateFastJob` (`income`, `time_window`, `xp_req`, `cooldown_days`) + a jobs app; Bank config (`interest_rate`).
- **Runtime:** jobs app render + `StartFastJob`/`FinishFastJob` (payout via `applyAndNotifyTrait`, `xp += 1`, cooldown via `delayDays`/day-key); Bank app (deposit/withdraw on the `money` trait + daily interest as a **G6 conditional daily_tick effect**). Time-of-day windows reuse the existing schedule primitive. Mirror to v1.
- **Accept:** a job pays out + grants XP + enforces its cooldown + respects its time window; bank balance accrues interest daily.

### G10 — PornCenter + xCam
**RTS:** PornCenter (genre × corruption browser; dormant even in RTS) + xCam (webcam: corr ≥4 + a `webcam` item) (doc 42 §6.4, §6.6).
- **Build on earlier tiers:** PornCenter ≈ **G8 gallery** gated by **G7 corruption tiers** (genre rows at 5/10/15/20); xCam ≈ a **G12 custom app** + a content scene, with the device gated like **G11** (a `webcam` item + corruption level).
- **Accept:** a corruption-tiered content browser; an xCam screen reachable once its hardware/corruption gate is met.

---

## Implementation order & framing
Implement and ship **tier by tier** — each is independently usable and verifiable:
1. **Tier 1 (G1, G6, G3)** — extends existing systems; immediately makes chat feel RTS-like.
2. **Tier 2 (G2, G5, G4)** — the social + story spine; introduces the two new subsystems (delay queue, quests).
3. **Tier 3 (G7, G8, G12, G11, G9, G10)** — the remaining apps; G7/G8/G11/G12 are small-medium and unlock G10 cheaply; **G9 is the one genuinely large build**.

Literal 100% parity requires all twelve. Most player-facing value lands in Tiers 1–2.

---

## Verification (whole-PRD, once Tier work is done)
- Build a fixture/TLS game that enables `[phone]` exercising each new field; `package_from_toml` clean.
- `pytest` green incl. all new schema + integration tests; v1/v2 parity (byte-equality regression) intact.
- Twee inspection: new condition types, quest macros, delay queue, daily_tick conditions present in emitted JS.
- Browser live-play: G1 toast on delivery; G6 conditional rise; G3 photo lock/cooldown; G2 posting→followers→milestone DM; G4 quest start→complete + journal; G5 scheduled event fires on day N; G7 tier gate; G8 gallery unlock; G11 purchase gate; G9 job payout + bank interest.

---

*Anchors: `apps/game_generation/twee_comprehensive/generators/v2.py` (1325, 1344, 1494–2166, 2942–3133, 4437–4477, 4715, 4772, 13520) + `v1.py` (parity); `apps/projects/services/template_import.py` (173–252, 345, 1593–1696); tests `apps/projects/tests.py` (546, 577, 696) + `apps/game_generation/tests.py`; docs `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md`. Targets: doc 42 (RTS) / doc 43 (engine as-built) / doc 44 (gap spec).*
