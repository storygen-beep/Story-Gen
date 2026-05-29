# Doc 46 — TLS Phone Design (chat-centric, RTS-faithful)

**Date:** 2026-05-22
**Type:** Design (authoring spec) — **no engine work, no TOML authored yet**. Builds on doc 42 (RTS phone target + §10 design philosophy), docs 43/45 (the shipped engine phone — every field below exists). Maps the RTS phone onto The Long Summer's actual content.
**Status:** ✅ **IMPLEMENTED 2026-05-22.** Authored into `7_final_game.toml`: `phone_active`+`frank_terms_accepted` flags, the acquisition hook (phone reactivates at the diner hire, alongside `hired_at_diner`), a hidden `npc_unknown` contact for the cam-hook, and the full `[phone]` block — Messages app + 9 conversations (frank_after_catch / frank_sleepover / frank_after_office[dormant] / jake_sorry / jake_tease / ryan_thanks / ryan_partner / anon_1 / anon_2) + 3 daily small-talk + 5 photo quick-actions. Build clean (no new warnings); live-play GREEN (phone gated on `phone_active`; `frank_after_catch` available on `frank_caught`; anon_1 false@corr0 → true@corr45; photo gates selfie/45/85; "Unknown" name resolves). Phase files NOT mirrored (7_final = build input). Follow-ups: photo art, the dormant office thread, optional Diana/Cookie threads.

**Scope decisions (user, 2026-05-22):**
- **Chat-centric core** only — Messages app (NPC threads + daily small-talk + photo quick-actions) + the anonymous-DM thread. **No** social feed, jobs, bank, gallery, or quests app.
- **RTS-style purchase gate** — the phone is acquired in-world (hidden until a flag is set).
- Voice follows TLS's RTS-flat scene style (speaker tags + short lines), which the engine's message-bubble chat renders natively.

> Every TLS trait/flag/threshold below is verified against `games/the_long_summer_test/toml_phases/7_final_game.toml`. No invented flags. Every engine field is one docs 43/45 actually shipped.

---

## 1. Why a phone here, and what it is NOT

RTS's phone is a **second hub** packaging *solo/remote* loops. TLS is a small, broke, trapped corruption slice — Maya has no fame fantasy, no follower economy, no porn-career arc. So we keep only the part of RTS's phone that fits TLS's premise: **the chat that carries the three men and the watcher.** We deliberately drop:

| RTS app | Dropped because |
|---|---|
| Social feed / Instafame (followers) | TLS has no `followers` trait or influencer fantasy; Maya is hiding, not performing for a public. |
| Fast Jobs / Bank | TLS already has a diner job + rent economy *in-world*; a phone economy would duplicate it and dilute the money-pressure that lives at the diner. |
| Naked Life / PornCenter / xCam | Out of slice scope; the one voyeur thread we want is the seeded **anonymous DM**, handled as a chat thread. |
| Quests app | TLS already has a `story_arc` hint/journal; a second journal would duplicate it. |

The phone in TLS = **Messages, and only Messages.** Its job is to make the three men (and the anonymous watcher) reach into Maya's pocket between in-person scenes, and to give her corruption a *remote* outlet (sending photos).

## 2. Design philosophy carried over (from RTS doc 42 §10)

The **evidenced** RTS principles that apply directly:
- **Earned / progressively disclosed.** The phone itself is gated behind acquisition (§3); each conversation thread appears only when its arc flag is set; photo actions unlock by corruption.
- **Telegraphed gates.** A locked photo action shows 🔒 + the reason (engine G3 `corruption_min` note); the anon-DM spicy branch shows its corruption requirement, not a silent block.
- **Daily cadence.** Small-talk is once-per-NPC-per-day; each photo action is once-per-day (engine `cooldown="per_topic"`). Paces the phone to the sleep loop, same as RTS.
- **Condition-gated delivery (the dispatch bus).** The engine re-evaluates every conversation trigger on each passage render and "dings" newly-available threads — TLS gets RTS's invitation-bus behavior for free by attaching triggers to arc flags.
- **Corruption as the escalation spine.** Photo tiers and the anon thread gate on Maya's raw `corruption`, the same axis the clothing shop and Frank arc already ride.

Reasonable inferences we adopt (not RTS facts, but they fit): the phone makes downtime *productive* (warm a relationship by text when you can't reach the NPC in person), and it's a **private** surface where Maya acts on her corruption herself rather than only receiving it in-world.

## 3. The device + acquisition (engine G11 `purchase_flag`)

**`[phone] purchase_flag = "phone_active"`** — the sidebar 📱 button stays hidden until the player flag `phone_active` is set.

**In-world acquisition beat (proposed).** Maya's prepaid line is dead — she's broke (premise). Two authored ways to set `phone_active`, pick one when authoring:
- **(A, recommended) Self-reactivation:** after the first diner pay (she has `money`), a one-time choice/beat "top up your phone" deducts a small sum and sets `phone_active`. Reinforces money-pressure → she spends scarce cash to stay connected. Hang it off `hired_at_diner` (verified flag) + a money cost.
- **(B) Frank covers it:** an early beat where Frank "takes care of the bill" — sets `phone_active` and a small Frank `love`/leverage seed. Darker, more RTS-landlord. Hang off `arrived_at_franks` / `first_morning_kitchen_done` (verified flags).

Either way it's a **single new flag** + one authored choice; no engine change. The phone realistically arrives Day 1–2, so most of the slice has it.

## 4. App roster

One app:
```toml
[[phone.apps]]
id    = "messages"
type  = "chat"
label = "Messages"
```
(No other apps — per scope. `purchase_flag` lives on the top-level `[phone]` table.)

## 5. Chat conversation map (the spine)

Each `[[phone.conversations]]` = a thread that **appears when its trigger flag is set** (the bus), runs scripted message bubbles + branching `reply` rounds, and whose reply choices apply `effects` (trait) + `flagEffects` (flag) — identical primitives to canvas choices. All triggers use the engine convention `trigger = { conditions = { version="1.0", items=[...] } }`.

| id | npc | trigger (verified flag) | beat | rounds | reply effects |
|---|---|---|---|---|---|
| `frank_after_catch` | npc_frank | `frank_caught` | "The arrangement" — Frank lays down the new terms the morning after the couch catch | 1 | accept → Frank `trust +`, set `frank_terms_accepted`(new); push back → Frank `trust −`, seeds rupture |
| `frank_after_office` | npc_frank | `frank_office_first_sex_done` | clipped morning-after; ownership tone | 1 | submit → Frank `love +`; deflect → Frank `corruption +` |
| `frank_sleepover` | npc_frank | `frank_sleepover_done` | routine established; "this is how it is now" | 1 | lean in → Frank `love +`, seed keep-route-romantic; stay cool → seed keep-route-arrangement |
| `jake_sorry` | npc_jake | `jake_peek_draw_revealed` | shy artist apologizes for the peek; offers to "draw you properly" | 2 | warm → Jake `trust +`; bold → Jake `corruption +` |
| `jake_tease` | npc_jake | `jake_tease_open` | escalating flirt; he's nervous, she's in control | 2 | tease → Jake `arousal +`, Maya `corruption +`; pull back → Jake `trust +` |
| `ryan_thanks` | npc_ryan | `ryan_help_tier_open` | warm thank-you after she helps at the shop | 1 | friendly → Ryan `trust +`; flirty → Ryan `love +` |
| `ryan_partner` | npc_ryan | `ryan_partner_open` | "be my partner on this" — the straight, kind alternative | 2 | yes → Ryan `love +`, seed keep-route; not yet → Ryan `trust +` |
| `anon_1` | (stranger, `poster_name="Unknown"`) | `corruption gte 45` (the verified TLS lewd threshold) | cold opener: "I've seen you. I'll pay to see more." sets `anon_dm_seen` | 2 | engage → Maya `corruption +`; block → no effect (reversible) |
| `anon_2` | Unknown | `anon_dm_seen` true AND `corruption gte 85` | the offer escalates (cam/meet hook) — **telegraphed**: spicy accept shows the corruption requirement | 3 | accept branch gated; sets a Phase-3 seed flag; refuse → light |

Notes:
- New flags introduced by the design (all author-side, no engine change): `frank_terms_accepted`, plus reuse of existing keep-route seed flags where they already exist.
- ~~The two Frank "keep-route" threads (romantic/arrangement) reuse the slice's existing `frank_keep_route_*` seed flags rather than inventing new endings.~~ **CORRECTED 2026-05-27 (Doc 70 §4.3 / §6.1.1):** the `frank_keep_route_*` declarations were RETIRED by Doc 19 ("No `frank_keep_route_*` flags") and flagged for removal by Doc 20. Doc 46 mistook the orphaned declarations for live infrastructure. The `flagEffects` lines + the 4 declarations were removed from `7_final_game.toml` on 2026-05-27. Frank chat reply trait deltas are preserved; the Frank "keep-route" routing surface is closed at slice scale. Ryan `keep_route_*` flags remain in place (Cˢ Seed per Doc 58).
- `anon_*` is the only non-NPC thread; it is the seeded `anon_dm_seen` cam hook made systemic. It is **corruption-gated, not flag-chain-gated**, so it surfaces exactly when Maya is corrupt enough — pure RTS secret-admirer pattern.

## 6. Daily small-talk (`[[phone.daily_topics]]`)

Per NPC, **1 chat per NPC per day** (engine default cadence), stage-gated by arc flags, small relational effects. The *remote* counterpart to TLS's in-person `talked_<npc>_today` gates — texting warms the bond when you can't reach them in person.

- **Frank** (gated `frank_caught`): terse check-ins ("you eat?", "door's unlocked"). `trust +1` or `love +1`.
- **Jake** (gated `jake_peek_draw_revealed`): art talk / shy banter. `trust +1`; occasional `corruption +1` on a flirty option.
- **Ryan** (gated `ryan_help_tier_open`): warm, easy. `love +1` / `trust +1`.

Each topic carries `conditions` so it only offers when the relationship is at the right stage; effects are small (the big jumps live in the scripted threads + in-person scenes).

## 7. Photo quick-actions (engine G3, `cooldown="per_topic"`)

Inside each man's thread, Maya can send a photo — the **corruption-as-agency** loop, RTS's selfie/lewd/nude with TLS thresholds aligned to the clothing economy:

| action | gate (`corruption_min`) | effects on send |
|---|---|---|
| Send a selfie | none | Maya `arousal +1`; NPC `love`/`trust +1`; per-NPC reply line |
| Send a lewd photo | **45** (= TLS Cute-clothing / verified `corruption gte 45`) | Maya `arousal +1`, `corruption +1`; NPC `arousal +1` |
| Send a nude | **85** (= TLS Bold-clothing tier) | Maya `arousal +1`, `corruption +2`; NPC `arousal +1`, `corruption +1` |

- Locked actions render 🔒 + "You aren't bold enough yet" (telegraphed). Each is once/day (`cooldown="per_topic"`), so the player rations them across the day-loop.
- Replies are per-NPC (Frank's possessive, Jake's flustered, Ryan's sweet) via the engine's `daily_topics` photo-action reply text.
- These are the **seeders**: always reachable (no flag chain), so corruption/arousal can always climb — anti-soft-lock per RTS doctrine.

## 8. Delivery, notification, anti-soft-lock

- **Dispatch bus:** the engine evaluates every conversation/anon trigger on each passage render; a newly-satisfied thread bumps the unread badge and fires a `notify` "ding" (e.g. Frank: *"Frank texted you."*; Unknown: *"New message."*). Authored per-conversation `notify` strings.
- **Anti-soft-lock:** small-talk + the selfie photo action are always reachable once the phone is active, so Maya can always raise corruption/arousal toward the next gate; nothing requires a state she can't reach.
- Phone is hidden pre-acquisition (`phone_active`), so no empty-phone confusion early.

## 9. Voice & format

RTS-flat message bubbles (the engine renders `message`/`reply` blocks as a chat). Keep TLS register:
- **Frank** — clipped, declarative, possessive. Short. "Door's unlocked." "You're mine now. Act like it."
- **Jake** — lowercase, hesitant, trailing. "i didn't mean to look. you're just… yeah."
- **Ryan** — warm, easy, decent. "Thanks for today. You're good people, Maya."
- **Unknown** — cold, transactional, no warmth. "I'll pay. You'll like the number."

Per ENI rules, allow one short *italic* private thought where a bubble can carry it (kept brief — chat bubbles are terse). Bodies stay RTS-flat per the TLS scene-style memory, not prose-dense.

## 10. Authoring notes (for the implementation pass)

- **Trigger nesting:** every `trigger` / gallery / post must be `trigger = { conditions = {...} }` — the engine reads `trigger.conditions` (doc 43 gotcha). The most likely first-pass bug.
- **Corruption is raw points**, not RTS tiers — gate on `{type:"trait", trait_key:"corruption", operator:"gte", value:45}` (and `corruption_min:45` on photo actions). Do NOT use `corruption_level` unless we also define `[engine].corruption_tiers` for TLS.
- **One new flag** (`phone_active`) + optional `frank_terms_accepted`; everything else reuses verified existing flags.
- **Mirror canonical bits** to the phase files per the clothing/arousal precedent (7_final is the build input + source-of-record).
- **Verify pass:** `package_from_toml` clean → twine-game-explorer: phone hidden until `phone_active`; threads ding on their flag; photo actions lock <45 / unlock ≥45; small-talk 1/day; anon thread surfaces at corruption 45.

---

*Companions: doc 42 (RTS phone + philosophy), doc 43 (engine phone reference), doc 45 (parity build). Source inventory: `games/the_long_summer_test/toml_phases/7_final_game.toml`. No TOML authored in this doc — design only.*
