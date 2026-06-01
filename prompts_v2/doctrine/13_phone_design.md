# Doctrine 13 — Phone & Apps Design

**Sources:** Engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (phone init `:995–1102`, `$game_state.phone` state `:1147`, delivery scan `setup.checkPhoneConversations` `:1659`, thread grouping `getPhoneThreads` `:1722`, chat render `openChatThread` `:1972`, reply effects `sendPhoneReply` `:1772`, daily-chat/photo `sendDailyChat` `:1844`, social feed `:2165`, dating `:2268`, gallery `:2410`, sidebar button widget `phoneButton` `:14695`, **trigger evaluator `triggerConditionsSatisfied` `:3308`**) + `apps/projects/services/template_import.py` (read `:2394–2517`, `TemplatePhone` dataclass `:286`); TLS gold-standard `[phone]` (`games/the_long_summer_test/toml_phases/7_final_game.toml` — 9 threads + small-talk + photo actions); Late Shifts phone build (2026-06-02 — `games/late_shifts/toml_phases/8_phone.toml`, the first prompts_v2 game to ship a phone); Phase-2 design docs (`28th_april_TLS_Phase2_Redesign/42_RTS_Phone_System_Reference.md`, `43_Engine_Phone_System_Reference.md`, `44_RTS_Phone_Parity_Gap_PRD.md`, `45` parity build, `46_TLS_Phone_Design.md`); a live re-play of RTS (road-to-success v0.26) confirming the device model.
**Authority:** Doctrine. WHEN to use the phone, which app types to reach for, and how to wire threads so they actually fire. Schema lives in `schema/02_toml_schema.md` §13; this file is the design model.
**Purpose:** The engine ships a complete phone (Doc 45 implemented all 12 RTS-parity gaps), but it's easy to wire so the button never appears (the scoping trap), threads never dispatch (dead-flag triggers), or a reminder uses a condition type the evaluator doesn't support (the `day`/`time` trap). This file encodes the verified model.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[phone]` enable switch), §13 (field tables + the trigger-condition vocabulary); `schema/03_example_toml.md` §14 (verbatim worked block); `doctrine/11_clothing_design.md` §8 + `doctrine/12_rent_economy_design.md` §8 (sibling scoping traps); `doctrine/01_rts_principles.md` (earned progression); `stages/02_toml_generation_prompt.md` Step 1 (`[phone]` emission).

---

## §1 — The phone is the digital surface (RTS parity)

**Rule: use the phone when the world has off-location interactions — texts, posts, a digital economy — that should reach the player anywhere, on a daily cadence, gated by the same corruption spine as the rest of the game.**

RTS makes the phone a second world layer: a purchased device (a $400 item; the sidebar button appears only once owned — re-verified live on v0.26) holding Messages, a follower economy, fast jobs, a bank, a gallery, and a quest journal. Its threads are instanced by a daily dispatch tick and gated by relationship + corruption + day state; 52 NPCs each carry `relation / corruption / arousal / talkedToday`, so corruption is the escalation spine and `talkedToday` the daily-cadence throttle (Doc 42; live source inspection). The engine reproduces this model with TOML primitives (Doc 43/45).

Use the phone when: NPCs would plausibly text; the game has a follower/job/bank economy worth a screen; or escalation wants a private channel (lewd photos, an anonymous watcher) parallel to in-location scenes. Skip it for a single-location game with no off-screen life. The phone is a *surface*, not an arc — it carries arcs authored elsewhere into a place the player checks between scenes.

---

## §2 — What the engine gives you for free

You author config + content; the engine owns all the logic (full schema: `schema/02` §13).

- **The device + gate.** A sidebar 📱 button renders when `enabled` is true AND (`purchase_flag` is empty OR `flags[purchase_flag]` is set). Unread count shows as a badge. (`:14695`.)
- **Delivery.** `checkPhoneConversations()` runs every passage render: it scans conversations/posts/profiles, marks any whose `trigger` is now satisfied, and (after a baseline first scan) fires a toast using the item's `notify` string (`:1659`). No author loop needed — content arrives when its conditions go true.
- **Threads.** Chat apps group conversations by NPC into threads (name + portrait + unread), newest-first (`:1722`). Each thread renders its blocks as bubbles + reply buttons, with a typing animation for pending NPC messages (`:1972`).
- **Reply effects.** A reply choice applies `effects` (traits), `flagEffects`, `questEffects`, `scheduleEffects`, shows a toast, and re-renders (`:1772`) — the same effect primitives as canvas choices.
- **Small-talk + photo actions.** `daily_topics` give repeatable per-day chat with cooldown + corruption gating (`:1844`).
- **Other apps.** social_feed (read + player posting), dating (swipe/match), gallery, custom (renders a passage), quests, fast_jobs, bank — all author-configured (Doc 45).
- **Persisted state** in `$game_state.phone` (triggered/read/replies/posts/profiles/matches) + `daily_chats` (`:1147`).

What the engine does NOT give you: a day-of-week trigger (§4), validation of reply-effect field names (author them correctly), or any thread that reads rent's `is_due` state (§4).

---

## §3 — Chat-thread design (trigger on REAL flags)

**Rule: trigger every conversation on a condition that actually goes true in your game — an arc flag with a verified setter, or a trait threshold — or the thread is dead weight that never dispatches.**

A conversation's `trigger.conditions` decides when it arrives. The single most common failure is triggering on a flag nothing sets (the dead-flag trap, same as canvas triggers). Author threads against the arc flags you already set:

- **TLS:** threads gate on `frank_caught`, `jake_peek_draw_revealed`, `ryan_partner_open` — real arc-stage flags. The anonymous watcher gates on raw `corruption gte 45` (a trait, not a flag) so it surfaces from player state alone.
- **Late Shifts:** Cole/Hank/Ben threads gate on `cole_noticed`, `hank_first_contact`, `ben_consummation_done`, etc. — each a verified setter in the arc.

Thread shape:
- **Multi-round.** Blocks carry `round`; a `reply` block presents choices; later `message` blocks gate on `after_round` + `after_choice` to branch on what the player picked. Keep branches short — a thread is a text exchange, not a scene.
- **Effects match the NPC's traits.** A reply effect must target a trait the NPC actually has. Cole (relation only) gets `relation` effects; Hank/Ben (arousal) can get `arousal`; only corruption-bearing NPCs get `corruption`. A phantom-trait effect is silent noise.
- **Register.** Threads are mostly one-shot (the engine marks them read), so they can carry a little more texture than a re-readable hub — but stay in the NPC's voice and keep it terse; texts aren't prose passages (`doctrine/05`).

---

## §4 — Trigger condition vocabulary (the `day`/`time` trap)

**Rule: phone triggers use ONLY the types the `triggerConditionsSatisfied` evaluator supports. It does NOT support day-of-week or clock time. For time-relative delivery use `days_since_flag`.**

This is the section that prevents a real, easy-to-make bug. The phone (and posts, profiles, daily_topics) all evaluate triggers through `triggerConditionsSatisfied` (`v2.py:3308`). Source-verified supported `items[].type`:

`flag` · `trait` · `days_since_flag` · `pass` · `item` · `stage` · `quest` · `corruption_level` · `modifier` · `clothing_slot` · `clothing_item` · `worn_beauty` · `worn_corruption` · `worn_type`

**NOT supported here: `day`, `time`, `weekday`, `location`, `random`.** Those exist only in the *canvas* trigger path, not the phone evaluator. Do not author a phone thread that fires "on Friday" or "at night" — it will never match.

For time-relative content, use **`days_since_flag`**: it fires N days after a flag's recorded `set_day` (`{type="days_since_flag", subject="player", flag_key="hired_at_diner", operator="gte", value=4}`). Late Shifts uses exactly this for Vince's rent nudge — phone triggers can't read rent's live `is_due` state, so a "Friday's close" reminder lands ~4 days after hire (near the first rent week) via `days_since_flag`, and the eviction consequence thread gates on the real `rent_evicted` flag. That is the honest substitute for a day-of-week trigger.

(Historical note: earlier corpus drafts listed `day`/`time`/`location`/`random` as phone condition types. They are fictional for this path — corrected 2026-06-02 against source.)

---

## §5 — Small-talk vs photo quick-actions (`daily_topics`)

**Rule: `daily_topics` is the repeatable side-channel — low-stakes chatter and corruption-gated photo actions, never a capstone. Tier photo actions by `corruption_min`; throttle each with `cooldown`.**

`daily_topics` are the phone's everyday texture, distinct from one-shot conversations:

- **Small-talk:** `player_message` + `npc_response` + small `effects` (relation ±1), gated by an arc flag, default cooldown = once per NPC per day. Ambient warmth, not plot.
- **Photo quick-actions:** the same primitive with `cooldown = "per_topic"` (each action its own 1/day cap, so selfie + lewd + nude can each fire once daily) and `corruption_min` tiers. The RTS-faithful ladder is **selfie (no gate) → lewd (`corruption_min = 45`) → nude (`corruption_min = 85`)** (Doc 45 G3; TLS + Late Shifts both use it). Tiers telegraph: a locked action shows the requirement, so the player sees the next rung. Effects climb with the tier (player arousal/corruption + NPC arousal), and — as in §3 — only target traits the NPC carries.

Photo actions are the chat-side analogue of RTS's sendSelfie/sendLewd/sendNude. They are escalation surfaces, not story beats; the story beats they reward live in the canvases.

---

## §6 — App-type decision rule

**Rule: reach for the smallest app set that carries the game's off-location life. Most arc-driven adult games are chat-centric — one `chat` app is often the whole phone.**

Valid `type`s (`schema/02` §13.2): `chat` · `social_feed` · `dating` · `gallery` · `custom` · `quests` · `fast_jobs` · `bank`.

| App | Use when | Skip when |
|---|---|---|
| `chat` | NPCs text; private escalation; the default phone surface | almost never (this is the core) |
| `social_feed` | a follower/reputation economy (post selfie/lewd/nude → followers via `post_actions`) is a real drive — the Instafame fantasy | no fame arc; it becomes an empty wall |
| `dating` | meeting NPCs via swipe/match is a mechanic, not just narrated | the cast is fixed and met in-world |
| `gallery` | unlocked media is a collectible reward track | no media-reward loop |
| `custom` | a bespoke screen (renders an author passage) | a standard app fits |
| `quests` | the V2 quest journal should live on the phone | quests surface elsewhere |
| `fast_jobs` / `bank` | the money economy wants in-phone jobs + interest (RTS-scale) | rent + a sidebar money band is enough |

RTS surfaces six apps on its home grid (Messages, Quests, Fast Jobs, Statistics, Gallery, Bank — live v0.26; Instafame/xCam are laptop/feature subsystems). TLS and Late Shifts deliberately ship **chat only** (Doc 46): a trapped corruption slice has no fame economy or job-board fantasy, so the social_feed/dating/jobs/bank apps would be empty rooms. Match the app set to the game's actual systems — an app with no content reads as broken.

---

## §7 — `purchase_flag`: the acquisition beat (earned device)

**Rule: gate the phone behind `purchase_flag` so the device is *acquired*, not assumed — RTS-faithful earned-progression pacing. The flag needs exactly one reachable setter.**

In RTS the phone is bought ($400); the sidebar button doesn't exist until you own it. The engine models this with `purchase_flag`: the button is hidden until `flags[purchase_flag]` is set. This gives a deliberate "phone arrives" moment instead of a phone from frame one.

- **TLS / Late Shifts:** `purchase_flag = "phone_active"`, set at the diner hire — the cut-off phone reconnects once there's income. One setter, on the hire choice.
- Like any `is_true` flag, `purchase_flag` must have a setter the player will hit (the same rule as every gate flag, `doctrine/04`). Leave `purchase_flag` empty only if the phone should be present from the start (rare for RTS-style pacing).

The acquisition beat is also a natural pacing gate for everything on the phone: threads authored against early arc flags simply won't have a surface until the phone is active, which is usually what you want (the device and the first arcs arrive together).

---

## §8 — Enabling checklist + the scoping trap

The phone is OFF until a `[phone]` table turns it on, and the switch is a **silent-failure trap** if mis-scoped (the same family as clothing `doctrine/11` §8 and rent `doctrine/12` §8).

- [ ] **Top-level `[phone]` table, NOT a bare key, NOT under `[settings]`.** `enabled` lives under a `[phone]` header (read at `template_import.py:2394`; defaults true when the table is present). A bare `phone_enabled` key is dead config the importer never reads — it silently shipped a phoneless Late Shifts until 2026-06-02. (Clothing → `[settings]`, rent → `[settings.rent]`, phone → `[phone]`: three systems, three different homes.)
- [ ] **At least one `[[phone.apps]]`** with a valid `type` (§6); conversation `app` fields reference an app `id`.
- [ ] **Every conversation `trigger` is satisfiable** — flags have verified setters; no `day`/`time`/`location`/`random` types (§3, §4).
- [ ] **`days_since_flag` for time-relative delivery**, not a day-of-week condition (§4).
- [ ] **Reply/topic effects target real traits** — present on that NPC (§3); the player's `corruption`/`arousal` exist; no phantom traits.
- [ ] **`conversations[].npc` exists in `[[npcs]]`** (name + portrait come from the NPC).
- [ ] **Photo actions tiered + throttled** — `corruption_min` ladder, `cooldown = "per_topic"` (§5).
- [ ] **`purchase_flag` has exactly one reachable setter** (§7); empty only if the phone is present from turn one.
- [ ] **App set matches the game's systems** — no empty social_feed/dating/jobs apps (§6).

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[phone]` enable switch (the scoping fix).
- `schema/02_toml_schema.md` §13 — `[phone]` field tables + the trigger-condition vocabulary (§13.3).
- `schema/03_example_toml.md` §14 — verbatim phone excerpt (`[phone]` + thread + `days_since_flag` + photo action + the purchase gate).
- `doctrine/11_clothing_design.md` §8 / `doctrine/12_rent_economy_design.md` §8 — the sibling `[settings]`/`[settings.rent]` scoping traps.
- `doctrine/01_rts_principles.md` — earned progression + the corruption escalation spine the phone rides.
- `stages/02_toml_generation_prompt.md` Step 1 — `[phone]` emission.
- `28th_april_TLS_Phase2_Redesign/42_RTS_Phone_System_Reference.md` (RTS target), `43` (engine as-built), `44` (parity gaps G1–G12), `45` (parity build), `46` (TLS chat-centric design).

---

**End of file.** A phone that passes §8 is enabled correctly and aimed correctly: it gives off-location life a surface (§1–§2), delivers threads that actually fire on real flags (§3), uses only the conditions the evaluator supports (§4), throttles its repeatable actions and tiers them by corruption (§5), ships only the apps the game's systems justify (§6), and arrives as an earned device (§7).
