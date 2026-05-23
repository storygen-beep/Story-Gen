# Doc 43 — Engine Phone System Reference (as-built)

**Date:** 2026-05-21
**Type:** Engine authoring reference. Documents the **built-in phone system** in `twee_comprehensive` exactly as it exists today. Companion to doc 42 (RTS phone) and doc 44 (RTS-parity gap PRD).

> **Why this doc exists:** the generator ships a complete phone system that is **not documented** in `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` and is **not used in The Long Summer**. It IS used in production by `under_one_roof`, `two_weeks`, `new_in_town`, `jacks_world`. This doc makes it discoverable. Everything below is verified against source with `file:line` anchors. Code lives in **both** generators (`v1.py` frozen, `v2.py` default); all line cites are `v2.py`.

---

## 1. Enabling the phone

Add a top-level `[phone]` table to the game TOML:

```toml
[phone]
enabled = true

[[phone.apps]]
id    = "messages"
type  = "chat"
label = "Messages"

[[phone.apps]]
id    = "flaunt"
type  = "social_feed"
label = "Flaunt"
```

- Parsed by `template_import.py:1593–1696` into `TemplatePhone` (`template_import.py:246`), stored on `project.metadata["phone"]`.
- The generator reads `phone_settings` and only emits phone JS/CSS + the `$game_state.phone` state block when enabled (`v2.py:902, 1020, 1494`).
- A sidebar **📱 Phone** button is auto-added (`phoneButton` widget, `v2.py:13520`) with a live unread badge.

---

## 2. The shell

`setup.openPhone()` (`v2.py:1710`) builds a `.phone-overlay` modal containing a `.phone-frame`, a header, and an **app grid**. It is a pure DOM overlay layered over the current passage — **not** a passage navigation. Every sub-screen swaps content in place via `jQuery('.phone-frame').html(...)`, so opening an app, drilling into a thread, and backing out never leave the world passage. Close via the × or clicking the backdrop (`v2.py:2132, 2162`).

The unread badge is computed by `getPhoneUnreadCount()` (`v2.py:1539`) = unread triggered conversations + an unviewed feed.

---

## 3. App types

`VALID_PHONE_APP_TYPES = {chat, social_feed, gallery, dating, custom}` (`template_import.py:175`).

| Type | Status | Renderer |
|---|---|---|
| `chat` | ✅ implemented | `_renderThreadList` / `openChatThread` (`v2.py:1749, 1782`) |
| `social_feed` | ✅ implemented | `_renderSocialFeed` (`v2.py:1960`) |
| `dating` | ✅ implemented | `_renderDatingApp` (`v2.py:2012`) |
| `gallery` | ⚠️ **placeholder** | `_renderPlaceholder` → "Coming Soon" (`v2.py:2125`) |
| `custom` | ⚠️ **placeholder** | "Coming Soon" |

Each app is `{ id, type, label, icon }` (`template_import.py:178`). `icon` is optional (relative to the video folder); without it the grid shows the label's first letter.

---

## 4. Chat — `[[phone.conversations]]` (the deepest system)

### Schema (`template_import.py:186–205`)
```toml
[[phone.conversations]]
id  = "jake_bathroom_sorry"
app = "messages"          # which chat app
npc = "npc_jake"          # whose thread this lands in

[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "first_morning", operator = "is_true" }
] }

# Ordered blocks: "message" (npc/player bubble) or "reply" (player picks a button)
[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "hey"

[[phone.conversations.blocks]]
type = "reply"
round = 1
choices = [
  { text = "No worries 😊",            effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 1 }], flagEffects = [{ targetType = "player", flag = "jake_friendly_start" }] },
  { text = "Yeah I should've knocked.", effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 1 }], flagEffects = [{ targetType = "player", flag = "jake_boundaries_set" }] }
]

# Branching: this block shows only after round 1 was answered with choice index 0
[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "ok good"
after_round = 1
after_choice = 0
```
*(Verified worked example: `games/under_one_roof/toml_phases/6_final_game.toml:94+`.)*

Block fields (`TemplatePhoneConversationBlock`, `template_import.py:186`): `type` (`message`|`reply`), `sender` (`npc`|`player`), `content`, `choices[]` (for replies), `round`, `after_round`, `after_choice`, legacy `after_reply`.

### Runtime mechanics
- **Sequential gating** — an NPC's conversations render in order, but rendering **stops at the first unanswered reply** (`_hasPendingReply`, `v2.py:1799–1802`). The player must answer to advance the thread.
- **Multi-round branching** — replies are stored as `ps.replies[convId] = [{round, choice}, ...]` (`v2.py:1806`). Blocks gate on `after_round` (show only after round N answered) and `after_choice` (only if choice C was picked), enabling branching trees inside one conversation.
- **Answered rounds** show the locked-in player bubble; the open round shows reply buttons (`v2.py:1832–1858`).
- **Reply effects** (`sendPhoneReply`, `v2.py:1603`) — the chosen choice applies:
  - `effects[]` via `applyAndNotifyTrait` → trait `add`/`set` with optional `clamp`/`cap`, on `player` or `npc`.
  - `flagEffects[]` via `applyAndNotifyFlag` → flag `set`/`unset`/`toggle`.
  - **These are the identical effect/flag primitives canvas choices use.** A chat reply can move any trait and set any flag — and a flag gates locations (`entry_conditions`), canvases, hints, anything. This is the lever for "a text advanced the story."
- **Typing animation** — pending NPC bubbles animate with a typing indicator before appearing (`v2.py:1924–1955`).

---

## 5. Delivery (how conversations/posts/profiles "arrive")

`setup.checkPhoneConversations()` (`v2.py:1498`) runs on **every passage render** (called from the navigation hook at `v2.py:12810`). It scans all conversations, posts, and profiles; any not-yet-triggered one whose `trigger.conditions` are satisfied is **stamped triggered** (records day/hour) and bumps the unread badge.

So delivery is **condition-gated and continuously evaluated**: author a `trigger`, and the item appears the instant its conditions hold. **Caveat:** delivery only updates the badge — there is **no toast/"new message" notification** when something arrives (contrast RTS, which fires `createNotification`).

---

## 6. Daily topics — `[[phone.daily_topics]]` (repeatable chat)

```toml
[[phone.daily_topics]]
id = "ask_about_day"
npc = "npc_jake"
player_message = "how was your day?"
npc_response = "long. glad you asked though"
effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 1 }]
conditions = { version = "1.0", items = [ { type = "flag", subject = "player", flag_key = "jake_friendly_start", operator = "is_true" } ] }
```

Schema: `TemplatePhoneDailyTopic` (`template_import.py:236`). Mechanics (render `v2.py:1871–1914`, send `sendDailyChat` `v2.py:1669`):
- Inside an NPC thread, a "Say something…" row shows **up to 3** randomly-shuffled eligible topics.
- Eligible = `conditions` pass AND not already used; when all are used, the used-list resets (rotation).
- **Cadence: exactly 1 daily chat per NPC per day** — `canChat = npcDc.count < 1` (`v2.py:1883`), reset when `last_day_key !== currentDayKey` (`v2.py:1880`). Same day-key idiom RTS uses.
- Picking one pushes player+NPC bubbles into `daily_chat_history` and applies the topic's trait `effects`.

---

## 7. Social feed — `[[phone.posts]]` (read-only)

```toml
[[phone.posts]]
id = "jess_gym_post"
app = "flaunt"
poster_name = "@jessicafit_"   # stranger; OR set npc = "npc_x" for an NPC poster
image = "phone/posts/jess_gym.jpg"
caption = "leg day 🔥"
likes = 214
trigger = { conditions = { version = "1.0", items = [ ... ] } }
```

Schema `TemplatePhonePost` (`template_import.py:209`). Triggered posts render newest-first (`v2.py:1960`); opening the feed marks it viewed. **It is a consumption feed only** — no player posting, no follower counter (contrast RTS's post-to-gain-followers loop).

---

## 8. Dating — `[[phone.profiles]]` (swipe)

```toml
[[phone.profiles]]
id = "match_marco"
app = "dating_app"
npc = "npc_marco"
photos = ["phone/dating/marco1.jpg"]
bio = "gym, dogs, bad decisions"
age = "29"
interests = ["hiking", "tattoos"]
trigger = { conditions = { ... } }                 # when the profile appears
match_condition = { conditions = { ... } }          # whether liking → a match
```

Schema `TemplatePhoneProfile` (`template_import.py:222`). Tinder-style (`v2.py:2012`): shows the next un-acted triggered profile with like/pass. Like → if `match_condition` passes, adds to a "Matches" row + an "It's a Match!" overlay (`v2.py:2089`); else just records the like. Pass records the pass.

---

## 9. Persisted state

`$game_state.phone` (`v2.py:1020`):
```
{ triggered_conversations, read_conversations, replies,
  triggered_posts, viewed_feed,
  triggered_profiles, liked_profiles, passed_profiles, matches }
```
plus lazily-created `daily_chats` (per-NPC `{last_day_key, count, used_topics}`) and `daily_chat_history`. All save-persistent.

---

## 10. Authorable vs. not

| Capability | Authorable from TOML? |
|---|---|
| App grid (chat/social_feed/dating) | ✅ |
| Branching multi-round chat threads | ✅ |
| Reply choices that change traits + set flags | ✅ |
| Condition-gated delivery of conversations/posts/profiles | ✅ |
| Per-NPC daily repeatable chat (1/day) w/ conditions + effects | ✅ |
| Read-only social feed (NPC + stranger posts) | ✅ |
| Dating swipe + match conditions | ✅ |
| Unread badge | ✅ |
| Typing animation | ✅ (automatic) |
| `gallery` / `custom` apps | ❌ placeholder only |
| Player posting / follower counter | ❌ feed is read-only |
| "New message" toast on delivery | ❌ badge only |
| Player-initiated *new* threads / free text | ❌ player only taps authored reply buttons / daily topics |
| Quests, jobs, bank, money apps | ❌ not phone features (see doc 44) |

---

## 11. Follow-ups
- **`COMPREHENSIVE_SYSTEM_REFERENCE.md` does not document the phone.** A `[phone]` section should be added there so authors discover it. (Tracked separately.)
- For the gap to RTS's full phone and the work to close it, see **doc 44 (RTS Phone Parity Gap PRD)**.

---

*Source of record: `apps/projects/services/template_import.py:173–252, 1593–1696` (schema + parser); `apps/game_generation/twee_comprehensive/generators/v2.py:902, 1020, 1494–2166, 12810` (runtime); worked example `games/under_one_roof/toml_phases/6_final_game.toml:94`. Parity with v1.py confirmed.*
