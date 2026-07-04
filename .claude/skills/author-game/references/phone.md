# The phone system — the digital surface (chat / posts / photo economy)

Read this when the game has off-location life that should reach the player anywhere — NPCs who'd text,
a follower/photo-sale economy, a dating app, a gallery — and you're wiring the `[phone]` table. This is
the DESIGN + SHAPE model: what the engine gives you free, which conditions the phone evaluator actually
supports, and the three silent-failure traps (mis-scoped table, flat gate, fictional `day`/`time`
triggers). For the one-line index see `references/systems.md` (Phone row); for the build-breaker version
of the gate-nesting trap see `references/toml-gotchas.md` ("Phone gate nesting").

**Every engine claim here is verified against live code** (`v2.py` = comprehensive generator,
`template_import.py` = importer/validator) and the shipped `games/late_shifts/toml_phases/8_phone.toml`,
cited `file:line`. Where the engine and the old corpus draft disagreed, **code wins** and the divergence
is flagged inline `*(code-vs-lore note: …)*`.

## Contents
- §1 — When to reach for the phone
- §2 — What the engine gives you for free
- §3 — The trigger-condition vocabulary (the `day`/`time` trap) — the section that matters most
- §4 — `days_since_flag` — the only clock the phone has
- §5 — The gate-nesting trap (`trigger.conditions`, not flat) — cross-link
- §6 — `[phone]` scoping + `purchase_flag` (the device on/off)
- §7 — The app set + the content model (chat / posts / daily_topics / dating / gallery)
- §8 — Chat-thread shape (multi-round, branch, effects)
- §9 — The photo / post economy (selfie → lewd → nude)
- §10 — Import-time validation (what hard-fails)
- §11 — Enabling checklist

---

## §1 — When to reach for the phone

**Rule: use the phone when the world has off-location interactions — texts, posts, a digital economy —
that should reach the player anywhere, on a daily cadence, gated by the same corruption spine as the rest
of the game. Skip it for a single-location game with no off-screen life.**

The phone is a *surface*, not an arc. It carries arcs authored elsewhere (in canvases) into a place the
player checks between scenes. A thread fires when its arc flag goes true; a photo action escalates the
same corruption spine the canvases ride. Don't put a *new* arc on the phone — put the **digital echo** of
an arc there.

Reach for it when: NPCs would plausibly text (the default — a chat app is often the whole phone); the
game has a follower/photo-sale economy worth a screen; or escalation wants a private channel (lewd
photos, an anonymous watcher) parallel to in-location scenes. The shipped chat-only games (Late Shifts)
deliberately ship **no** feed/dating/jobs/bank apps — a trapped corruption slice has no fame economy, so
those apps would be empty rooms. **Match the app set to the game's actual systems (§7); an app with no
content reads as broken.**

---

## §2 — What the engine gives you for free

You author config + content; the engine owns all the logic.

- **The device + gate.** A sidebar 📱 Phone button renders when `phone_enabled` AND
  (`purchase_flag === ''` OR `flags[purchase_flag]` is set); an unread count shows as a `9+`-capped
  badge (widget `phoneButton`, `v2.py:15477-15487`). §6.
- **Delivery scan.** `setup.checkPhoneConversations()` runs on every passage render (called from the
  caption build, `v2.py:14623-14624` — the `StoryCaption` call site). It scans conversations, posts, and profiles; marks any whose
  trigger is now satisfied as triggered; and — after a baseline first scan — fires a toast using the
  item's `notify` string (`v2.py:1855-1900` — `checkPhoneConversations`). No author loop: content arrives the render its conditions
  go true. The first scan is silent so you don't get a wall of toasts at game start (`:1862` — `_firstScan` gate).
- **Threads.** Chat conversations group by NPC into threads (name + portrait + unread count), newest
  thread first, oldest message first within a thread (`getPhoneThreads`, `v2.py:1918-1966`). Each thread
  renders blocks as bubbles + reply buttons with a typing animation for pending NPC messages
  (`openChatThread`, `v2.py:2168+`).
- **Reply effects.** A reply choice applies `effects` (traits), `flagEffects`, `questEffects`, and
  `scheduleEffects`, shows a toast, marks the conversation read, and re-renders (`sendPhoneReply`,
  `v2.py:1968-2033`) — the same effect primitives as a canvas choice.
- **Daily small-talk + photo actions.** `daily_topics` give repeatable per-day chat with cooldown +
  corruption gating (`sendDailyChat`, `v2.py:2041-2090`; render `v2.py:2258-2316`).
- **Other apps.** `social_feed` (read NPC posts + player posting via `post_actions`), `dating`
  (swipe/match on `profiles`), `gallery`, `custom` (renders an author passage), `quests`, `fast_jobs`,
  `bank` — all author-configured, dispatched by `openPhoneApp` (`v2.py:2119-2134`).
- **Persisted state** in `$game_state.phone` (triggered/read conversations, replies, posts, profiles,
  matches, daily_chats, posted_days).

What the engine does NOT give you: a day-of-week or clock-time trigger (§3), validation that a reply
effect targets a trait the NPC actually has (author them correctly, §8), or any thread that reads rent's
live `is_due` state (§4).

---

## §3 — The trigger-condition vocabulary (the `day`/`time` trap)

**Rule: phone triggers use ONLY the types the `triggerConditionsSatisfied` evaluator branches on. It has
NO day-of-week, NO clock time, NO location, NO random. For time-relative delivery use `days_since_flag`
(§4).**

This is the section that prevents a real, easy-to-make bug. Conversations, posts, profiles, gallery
items, AND daily_topics all evaluate their gate through the **one** shared evaluator
`setup.triggerConditionsSatisfied` (`v2.py:3530`). It is the same evaluator canvases use — but the phone
delivery path passes it only what's in `trigger.conditions`, and that path can't inject the day/time
context the canvas path has. The supported `items[].type` set is **exactly** the `type === '…'` branches
in that function (`v2.py:3596-3864`):

| `type` | `v2.py` line | What it reads |
|---|---|---|
| `flag` | `:3596` | `$flags[key]` (player) or `npc.flags[key]` — `is_true`/`is_false`/`exists` |
| `trait` | `:3644` | a player or NPC `core_traits[key]` vs `value` (`gte`/`lt`/`eq`/…) |
| `days_since_flag` | `:3669` | days elapsed since a flag's `set_day` (§4) |
| `modifier` | `:3635` | a temporary modifier active/inactive |
| `pass` | `:3785` | a recurring pass active |
| `item` | `:3795` | inventory item count |
| `stage` | `:3808` | a named composite gate (`engine.stage_helpers`) — one-level recurse |
| `quest` | `:3824` | quest `active` / `completed` / `step_gte` |
| `corruption_level` | `:3836` | the banded corruption tier (`gte`/`lt`/`eq`) |
| `clothing_slot` | `:3706` | a slot equipped/unequipped *(clothing-enabled builds only)* |
| `clothing_item` | `:3723` | a specific item equipped/owned *(clothing-enabled only)* |
| `worn_beauty` / `worn_corruption` | `:3751` | MAX stat across the worn outfit *(clothing-enabled only)* |
| `worn_type` | `:3766` | an outfit category equipped *(clothing-enabled only)* |
| `npc_at_location` | `:3847` | cross-room presence — NPC present/absent at a location |

**NOT supported here — these never match, no build error:** `day`, `time`, `weekday`, `hour`, `location`,
`random`. They do not appear as branches in the evaluator (the final `// Unknown type` falls through to
`results.push(false)`, `v2.py:3866-3867`). Do not author a phone thread that fires "on Friday" or "at
night" — the item evaluates false forever and the thread is dead weight.

*(Code-vs-lore note: the old corpus draft's vocabulary list was close but **stale in two ways** — it
omitted `npc_at_location` (it was added 2026-06-17, `v2.py:3847`), and it is the cross-room
presence gate, so a thread CAN now fire on "she's home" / "the kitchen is empty". Older drafts than that
listed `day`/`time`/`location`/`random` as phone types — those are fictional for this path and always
were. The table above is the live branch set; trust nothing else.)*

**The fail-open backstop you still must respect:** the evaluator opens with
`if (!conditions.version || conditions.version !== '1.0') return true;` (`v2.py:3534`). A `conditions`
block lacking `version = "1.0"` is treated as **satisfied** — the items never checked. For a phone
thread that means it fires at game start. **Every `conditions` block needs `version = "1.0"`** (the
house-wide trap — `references/toml-gotchas.md`).

---

## §4 — `days_since_flag` — the only clock the phone has

**Rule: for time-relative delivery, use `days_since_flag` — it fires N days after a flag was set. It is
the honest substitute for the day-of-week trigger the phone doesn't have.**

The phone evaluator can't read the calendar, but it CAN read how long ago a flag went true.
`days_since_flag` compares `currentDay − flag.set_day` against `value` (`v2.py:3669-3703`); the set-day
comes from `$flags_meta[key].set_day`, recorded when the flag is set, so it only works on a flag that was
actually set in play (an unset flag → condition fails, `v2.py:3694` — `!flagValue || setDay === null`).

```toml
[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "days_since_flag", subject = "player", flag_key = "hired_at_diner", operator = "gte", value = 4 },
] }
```

Late Shifts uses exactly this for Vince's rent nudge (`games/late_shifts/toml_phases/8_phone.toml:272-275`):
the phone can't read rent's live `is_due` state, so a "Friday's close" reminder lands ~4 days after hire
(near the first rent week) via `days_since_flag`, and the eviction-consequence thread instead gates on the
real `rent_evicted` flag (`:295-298`). That pairing — `days_since_flag` for the *approach*, a real
arc/system flag for the *event* — is the pattern for any time-relative phone content.

---

## §5 — The gate-nesting trap (`trigger.conditions`, not flat)

**Rule: a phone conversation/post/profile gate nests ONE level deeper than a canvas trigger —
`trigger.conditions = { version, items }`. The flat canvas shape leaves `conditions` undefined → every
thread fires at game start.**

The delivery scan reads `conv.trigger.conditions` (`v2.py:1869-1870`), `post.trigger.conditions`
(`:1884-1885`), and `prof.trigger.conditions` (`:1895-1896`). The importer stores the whole `trigger`
table verbatim (`template_import.py:2433/2455` for conversations, `:2473` posts, `:2491` profiles) and
passes it through to `metadata["phone_settings"]` unchanged (`:5845`). So the engine looks specifically
for a `.conditions` **child** of `trigger`. Author it the canvas way — `version`/`items` flat directly
under `[phone.conversations.trigger]` — and `trigger.conditions` is `undefined`, the `if (trigCond && …)`
guard skips the check, and the thread is treated as already-satisfied. Result: every thread fires turn 1
and the badge shows them all.

```toml
[[phone.conversations]]
id  = "cole_opener"
app = "messages"
npc = "npc_cole"
[phone.conversations.trigger]          # ← the trigger TABLE
conditions = { version = "1.0", items = [   # ← .conditions CHILD (the gate)
  { type = "flag", subject = "player", flag_key = "cole_noticed", operator = "is_true" },
] }
```

Grep guard: the line after every `[phone.*.trigger]` header should be `conditions = {`. Full write-up +
the live case (The Inheritance, 3 end-state threads all fired turn 1) lives in `references/toml-gotchas.md`
("Phone gate nesting") — don't duplicate it; this section is the cross-link.

---

## §6 — `[phone]` scoping + `purchase_flag` (the device on/off)

**Rule: the phone config lives at a TOP-LEVEL `[phone]` table — NOT under `[settings]`, NOT a bare key.
Mis-scope it and the phone silently ships OFF (the same silent-failure family as clothing's `[settings]`
and rent's `[settings.rent]`).**

The importer reads `data.get("phone")` (`template_import.py:2411`) — a top-level table. `enabled` defaults
**true** when the `[phone]` table is present (`:2415`). A bare `phone_enabled` key is dead config the
importer never reads — it silently shipped a phoneless Late Shifts until 2026-06-02. Three systems, three
different homes: clothing → `[settings]`, rent → `[settings.rent]`, phone → top-level `[phone]`.

```toml
[phone]
enabled       = true
purchase_flag = "phone_active"
```

**`purchase_flag` — the earned device.** When set, the sidebar 📱 button is hidden until
`flags[purchase_flag]` is true (`v2.py:15478`; flag read from `phone_purchase_flag`, `v2.py:1131` /
`template_import.py:2533`). Empty string = button always shown (phone from frame one). RTS-faithful pacing
buys the phone (a "phone arrives" beat) instead of assuming it: Late Shifts sets `purchase_flag =
"phone_active"`, flipped at the diner hire alongside `hired_at_diner` — Maya's cut-off phone reconnects
once income is coming in (`8_phone.toml:14-18`). The flag needs **exactly one reachable setter**, like any
gate flag. The acquisition beat is also a natural pacing gate for everything on the phone: threads
authored against early arc flags simply have no surface until the device is active — usually what you
want (the device and the first arcs arrive together).

---

## §7 — The app set + the content model

**Rule: reach for the smallest app set that carries the game's off-location life. Most arc-driven adult
games are chat-centric — one `chat` app is often the whole phone. Each app `type` is validated at import
(§10); an app with no content reads as broken.**

Valid app `type`s (`VALID_PHONE_APP_TYPES`, `template_import.py:193`):
`chat` · `social_feed` · `gallery` · `dating` · `custom` · `quests` · `fast_jobs` · `bank`.

| App | The content array it renders | Use when | Skip when |
|---|---|---|---|
| `chat` | `[[phone.conversations]]` + `[[phone.daily_topics]]` | NPCs text; private escalation — the default surface | almost never (this is the core) |
| `social_feed` | `[[phone.posts]]` + app `post_actions` | a follower/reputation economy is a real drive (the Instafame fantasy) | no fame arc → an empty wall |
| `dating` | `[[phone.profiles]]` (swipe → match) | meeting NPCs via swipe is a mechanic, not just narrated | the cast is fixed and met in-world |
| `gallery` | `[[phone.gallery_items]]` | unlocked media is a collectible reward track | no media-reward loop |
| `custom` | an author passage (`app.passage`) | a bespoke screen | a standard app fits |
| `quests` | the V2 quest journal | quests should live on the phone | quests surface elsewhere |
| `fast_jobs` / `bank` | money jobs / interest | the money economy wants an in-phone screen | rent + a sidebar money band is enough |

The content arrays are all **top-level under `[phone]`**, keyed to an app by an `app` field that must match
an app `id` (validated, §10): `[[phone.conversations]]` (`app` → a `chat` app), `[[phone.posts]]` (`app` →
a `social_feed` app), `[[phone.profiles]]` (`app` → a `dating` app), `[[phone.daily_topics]]` (`npc`-keyed,
no `app` — rendered inside whichever chat thread matches the NPC), `[[phone.gallery_items]]`.

TLS and Late Shifts deliberately ship **chat only** — a trapped corruption slice has no fame economy or
job board, so the other apps would be empty rooms. Don't add an app you won't fill.

---

## §8 — Chat-thread shape

**Rule: trigger every conversation on a condition that actually goes true — an arc flag with a verified
setter, or a trait threshold — or the thread is dead weight. Keep it a text exchange, not a scene.**

A conversation is `id` + `app` (a chat app id) + `npc` (slug — name + portrait come from the NPC) + a
`trigger.conditions` gate (§5) + an optional `notify` toast string + an ordered `[[…blocks]]` list. Block
shape (`TemplatePhoneConversationBlock`, `template_import.py:208-217`):

- **`type = "message"`** — one bubble. Needs `sender = "npc"` or `"player"` and `content` (both validated,
  §10). `@player` / `@<npc>` tokens in `content`/`notify` resolve via `resolveAtRefs` at render
  (`v2.py:1877`, `:2217`).
- **`type = "reply"`** — presents `choices` (validated non-empty). Each choice carries `text` + the canvas
  effect primitives: `effects` (traits), `flagEffects`, `questEffects`, `scheduleEffects` — applied by
  `sendPhoneReply` (`v2.py:1997-2023`).
- **Multi-round / branch.** A `reply` block carries `round = N`; a later `message` block gates on
  `after_round = N` + `after_choice = K` so it shows only if the player picked choice K in round N
  (`template_import.py:215-217`; shipped branch: `8_phone.toml:69-80`). Keep branches short — a thread is
  a text exchange.

**Effects must target a trait the NPC actually has.** A reply effect against a phantom trait is a silent
no-op (the trait must be declared on that NPC — `references/trait-catalog.md`). Late Shifts is explicit:
Cole (relation only) gets `relation` effects; Hank/Ben (arousal) can get `arousal`; only corruption-bearing
NPCs get `corruption` (`8_phone.toml:40-41`, and every reply honors it). Threads are one-shot (the engine
marks them read), so they can carry a touch more texture than a re-readable hub — but stay terse and in
the NPC's voice; texts aren't prose passages.

---

## §9 — The photo / post economy

**Rule: tier the photo/sexting and feed-posting actions by a `corruption_min` ladder and throttle each
per day. These are escalation SURFACES, not story beats — the beats they reward live in the canvases.**

Two parallel mechanisms, both corruption-gated and daily-capped, both reading player `corruption`
directly:

**Photo quick-actions (in a chat thread) — `daily_topics` with `cooldown = "per_topic"`.** Each action is
its own once-per-day cap, so selfie + lewd + nude can each fire once daily (`v2.py:2059` — `per_topic` cooldown, render
`:2282-2289`). The RTS-faithful ladder is **selfie (no gate) → lewd (`corruption_min = 45`) → nude
(`corruption_min = 85`)** (Late Shifts `8_phone.toml:351-390`). A locked rung renders as
`🔒 [player_message]` so the player sees the next requirement (`v2.py:2285-2287` — `phone-daily-locked`). Effects climb with the
tier (player arousal/corruption + NPC arousal) and target only traits the NPC carries (§8). Distinguish
from **small-talk** `daily_topics` (no `cooldown` field) — those are the legacy per-NPC 1/day side-channel
(low-stakes chatter, `relation ±1`), arc-flag gated, ambient warmth not plot (`8_phone.toml:319-341`).
Each `daily_topic` may also carry its own `conditions` gate (`version = "1.0"` required, §3) checked at
render (`v2.py:2278` — `ptp.conditions` render check).

**Player feed posting — `post_actions` on a `social_feed` app.** The selfie/lewd/nude analogue for a
follower economy (`v2.py:2380-2402`, `sendSocialPost` `:2437-2463`). Each action:
`{ label, corruption_min?, daily_cap?, followers_min, followers_max, counter_trait }`. It's corruption-
gated (`🔒 label` when locked), daily-capped (default 1), and increments an author-named follower trait by
a random `followers_min..followers_max` (`counter_trait`, default `followers`). Reach for this only when a
follower count is a real drive (§7).

---

## §10 — Import-time validation (what hard-fails)

The phone path has real validation (`template_import.py:3433-3502`) — unlike most silent-failure systems,
these are loud build errors, so lean on them:

- **App:** `type` must be in `VALID_PHONE_APP_TYPES` (`:3446`); `id` must be snake_case (`:3441`), unique
  (`:3443`), and have a non-empty `label` (`:3450`).
- **Conversation:** `id` snake_case + unique (`:3484-3487`); `app` must reference a registered **chat**
  app id (`:3489` — a conv pointing at a `social_feed`/`dating`/non-existent app fails); `npc`, if set,
  must be a real NPC (`:3491`).
- **Block:** `type` must be `message`|`reply` (`:3495`); a `message` needs `content` (`:3497`) and
  `sender ∈ {npc, player}` (`:3499`); a `reply` needs non-empty `choices` (`:3501`).
- **Post:** `app` must reference a `social_feed` app id (`:3461`); `npc`, if set, must be real (`:3463`).
- **Profile:** `app` must reference a `dating` app id (`:3471`); `npc` real (`:3473`); `bio` required
  (`:3475`).

What validation does NOT catch (silent): a flat (un-nested) trigger gate (§5), a `version`-less conditions
block (§3 — fails open), a `day`/`time`/`location`/`random` condition type (§3 — evaluates false forever),
a reply effect against a trait the NPC lacks (§8 — no-op), or a thread gated on a flag nothing sets (the
dead-flag trap — verify your setters).

---

## §11 — Enabling checklist

- [ ] **Top-level `[phone]` table** (`enabled = true`), NOT `[settings]`, NOT a bare key (§6).
- [ ] **At least one `[[phone.apps]]`** with a valid `type` + snake_case `id` + `label` (§7, §10). Every
      content item's `app` field references an app `id` (chat→conversations, social_feed→posts,
      dating→profiles).
- [ ] **Every trigger nests as `trigger.conditions = { version = "1.0", items = [...] }`** — never flat
      (§5), always `version`-tagged (§3).
- [ ] **No `day`/`time`/`weekday`/`location`/`random` condition types** — `days_since_flag` for
      time-relative delivery (§3, §4).
- [ ] **Every conversation/topic trigger is satisfiable** — flags have verified setters; corruption/trait
      thresholds are reachable (§8).
- [ ] **Reply / topic / post effects target real traits** present on that NPC (or player corruption/
      arousal) — no phantom traits (§8).
- [ ] **Photo / post actions tiered + throttled** — `corruption_min` ladder (selfie/lewd/nude),
      `cooldown = "per_topic"` (photo) or `daily_cap` (post) (§9).
- [ ] **`purchase_flag` has exactly one reachable setter** (§6) — empty only if the phone is present from
      turn one.
- [ ] **App set matches the game's systems** — no empty social_feed/dating/jobs apps (§7).

---

**End of file.** A phone that passes §11 is enabled correctly (§6) and aimed correctly: it gives
off-location life a surface (§1–§2), delivers threads that actually fire on real flags nested the right
way (§5, §8), uses only the conditions the evaluator supports (§3) with `days_since_flag` for time (§4),
tiers + throttles its repeatable actions (§9), and ships only the apps the game's systems justify (§7).
