# Doc 42 — RTS Phone System Reference

**Date:** 2026-05-21
**Type:** RTS mechanism analysis (reference only — **no TLS proposals**). Sibling of docs 35 (state-variant doctrine), 36 (RTS-vs-engine clothing audit), 38 (RTS arousal). This doc describes how **Road to Success** builds its in-game phone; it does not propose anything for The Long Summer.

---

## 1. Provenance

Two explorer sessions on `https://mopoga.com/road-to-success` (slug `road-to-success`), combining live-play with a full extraction of the game's compiled JavaScript.

**Source artifacts** (all under `game_explorations/road-to-success/`):
- `_storyjs_dump.js` — the entire `twine-user-script` (507,773 chars, **111 numbered TS-compiled modules**). The authoritative source for every service.
- `passage_catalog.json` — all 358 passage sources (the SugarCube views/widgets).
- `notes.md` — the session research log (this doc is the cleaned synthesis of the three `PHONE DEEP-DIVE` note blocks).
- `_slice.py` — helper that slices a module out of the dump by its `twine-user-script #NN: "X.js"` header.

**Live-verified** (driven in-browser, not just read): phone purchase → sidebar button appears; modal opens; Messages thread seeded via `<<NewMessage>>`; corruption locks on `sendLewd`/`sendNude` flipping from 🔒 at corr 0 to open at corr 4; daily cooldown disabling `sendSelfie` after one send; the NPC auto-reply push.
**Source-read** (cited, not clicked): the day-tick dispatcher, the DM dialogue cascades, Naked Life / Fast Jobs / Bank / PornCenter / xCam internals.

---

## 2. The device shell & unlock

- The phone is a **purchased item**: `$items.phone = { price: 400, type: "electronics", icon: 📱 }`. At game start `player.inventory.phone = 0` (not owned).
- The sidebar `📱 Phone` button (in `StoryRightSidebar`) renders only `<<if isPurchased("phone")>>` — until you buy one, the button does not exist. Label gains a `✉️` and an unread count when `getUnreadPhoneThreadCount() > 0`.
- Clicking opens a **modal dialog** (`<dialog id="phone">` → `<<include "Phone">>`), **not** a passage navigation. The shell = status bar (`PhoneTop`: day cycle + clock) + app grid (`PhoneHome`) + a "Turn off" button that calls `resetPhoneUi()` + `closeDialog('phone')`.
- App icons render **conditionally**, so the launcher **grows with progression** (e.g. Instafame only after the account exists; Naked Life only after its account; the "New Messages (N)" button only when unread > 0).

### Two devices, not one
RTS deliberately splits remote activities across **two devices**:
- **Phone** — mobile, openable anywhere from the sidebar. Holds the social/economy/utility apps.
- **Laptop** (`Laptop` passage) — a **bedroom-only** desktop computer. Holds **Watch Porn** (gated `arousal ≥ 1`) and **xCam** (webcam). "Shutdown" returns to the bedroom.

The split encodes intent: things you'd plausibly do on the move live on the phone; things tied to being home (camming, watching porn) live on the laptop.

### Hardware-gate doctrine
Whole feature branches are gated behind **buying a device**. The phone ($400) unlocks the entire mobile suite. **xCam** additionally requires `isPurchased("webcam")` (a second item) **and** `getCorruptionLevel() ≥ 4`. Hardware purchase = a coarse, money-paced unlock on top of the corruption/quest gates.

---

## 3. Architecture

Clean **service-layer** separation, mirrored throughout the 111 modules:
- **Services** (`PhoneService`, `InstafameService`, `NakedLifeService`, `FastJobsService`, `PornCenterService`, `BankService`, `XCamService`, plus `TimeService`/`QuestService`/`CorruptionService`) hold all state and logic.
- **Controllers** (`PhoneController.js` etc.) register thin SugarCube macros (`<<NewMessage>>`, `<<RefreshMessages>>`, `<<AcceptNakedLifeChallenge>>`, …) that delegate to the service.
- **Passages** (`PhoneHome`, `Messages`, `Instafame`, `NakedLife`, `FastJobs`, …) are **dumb views** that read service data and render.

### App ↔ world coupling
Every app loop closes through a **world scene**. The phone app *sets up* an activity (unlocks a location, marks a challenge active, queues a job); the **world scene completes it and pays back** by calling the service:
- `FinishFastJob` ← `BabySitting` / `DogWalking` / `ElderlyCare` / `HouseCleaning1` / `HouseCleaning2`
- `completeNakedLifeChallenge` ← the flash scenes (`JoggingFlash`, `SwimFlash`, …)
- `AddInstafameFollowers` ← `Selfie`
- `FinishQuest` ← ~30 scenes (`SecretAdmirer`, `ModelPhotoshoot`, `JamalPoolGangbang`, `MarcusParkSex`, …)

The phone never *resolves* content; it dispatches and tracks. The world resolves.

---

## 4. The chat system (Messages)

### 4.1 Data model (`PhoneService`)
```js
player.phone.threads[] = {
  id, name,
  messages:    [ "JamalPoolParty::1779381357150::75385", ... ],  // instanced ids
  sentActions: [ { id, speakerId, text, imagePath?, dayUsed, timestamp }, ... ],
  actionUsageDays: { sendSelfie: <dayNum> },   // last-used day per action
  hasUnread: true
}
player.phone.selectedThread = "<open thread id>"
```
- **Message ids are instanced**: `createMessageEntryId` = `<templateId>::<Date.now()>::<rand>`. `getMessageTemplateId` strips back to the template. So one template can recur as multiple timeline entries.
- **Message bodies are authored widgets.** `RenderPhoneMessage(id)` resolves the template then wikis `<<{template}Message "id">>` — e.g. `<<JamalPoolPartyMessage>>`. Thread metadata catalog: `MESSAGE_THREADS = { JamalPoolParty→Jamal, VeronicaCostumeParty→Veronica, MarcusDate→Marcus }`.
- **Timeline** (`getThreadTimeline`) merges `messages` + `sentActions` into entries (`kind:"message"` / `kind:"action"`) and **sorts by timestamp**.

### 4.2 UI flow
Inbox (thread list; each button labelled `"<name> - N unread message(s)"` / `"<name> - Read"`) → open a thread → scroll the timeline → a **"Quick actions"** row of reply buttons. `selectThread` clears `hasUnread`; `clearSelectedThread` returns to the inbox.

### 4.3 The repeatable verbs + two gates
`THREAD_ACTIONS` are **global** (the same on every thread): `sendSelfie`, `sendLewd`, `sendNude`. Each action is evaluated against two independent gates:

| Action | 🔒 Lock (`PHOTO_ACTIONS.minCorruption`) | counter | Reply source |
|---|---|---|---|
| `sendSelfie` | none | `selfies++` | `THREAD_ACTION_REPLIES[thread].sendSelfie` |
| `sendLewd` | level ≥ 3 ("You aren't corrupted enough…") | `lewdSelfies++` | …`.sendLewd` |
| `sendNude` | level ≥ 4 | `nudeSelfies++` | …`.sendNude` |

- **🔒 Locked** = corruption tier too low; shows a `lockedNote`.
- **✦ Disabled** = `actionUsageDays[id] === game().game.days` → "Available tomorrow". **Daily cooldown, one send per action per day.** Retrying same day → notification "You already used this action today." (Verified live.)
- On send: pushes the player message (with a random `selfie/lewd/naked` image), increments the counter, then **auto-pushes the NPC reply** from `THREAD_ACTION_REPLIES[threadId][actionId]` (per-NPC voice; `_default` fallback). The *photo content is shared across NPCs; only the reaction line is personalized.*

So the service-thread chat is a **photo-sharing escalation loop** (selfie → lewd → nude) paced by corruption tier + a one-per-day cadence — not free-text or branching dialogue.

### 4.4 The two chat generations (they coexist)
1. **Service threads** (§4.1–4.3) — the dynamic timeline + quick-actions.
2. **Invitation widgets** (`PhoneMessages`) — the older system. `<<InvitationMessage stateKey npc invite accept decline declineReply>>` renders the NPC's invite and (once answered) the player's reply, keyed on `player.phone.messageStates[key] = "accepted" | "declined"`. The Accept/Decline **links live inside the message body** and only render while the state is `undefined` (idempotent).

A single thread can show **both** at once: e.g. the Jamal thread renders the pool-party invite bubble (with Accept/"I can't go" links) *and* the photo quick-actions below it.

### 4.5 Invite = a quest-control surface
The invitation links drive the quest engine directly:
- **Jamal** accept → `StartQuest PoolParty`.
- **Veronica** accept → `UpdateQuest CostumeParty` **branched on `$clothes.costume1.purchased`** (own the fairy costume → "go Saturday" step; else → "buy the costume at the mall" step).
- **Marcus** accept → `UpdateQuest MarcusDate`; **decline → `CancelQuest MarcusDate` + `ScheduleQuest MarcusDate 15`** (auto re-invites 15 days later).

---

## 5. The dispatch bus (how threads are *created*)

No passage fires `<<NewMessage>>`. Threads are pushed by the **day tick**. `TimeService.newDay()` runs an ordered pipeline:

```
resetGameCycle → rollDailyWeather → saveGame → improveMcMaximumStats →
resetPlayerStats → updateNPCs → updateLocations → resetLocationVariables →
checkSchoolTest → updatePregnancy → checkQuests → relationshipMessages →
baby/bank/property ticks → reduceDaysFromVariables → changeLaundryCut
```

`checkQuests()` and `relationshipMessages()` are where `PhoneService.newMessage()` fires — each guarded by `InventoryService.isPurchased("phone")` **and** a world-condition predicate:

| Message | Condition (all must hold) |
|---|---|
| `VeronicaCostumeParty` | `isQuestActive("CostumeParty")` && progress == 0 |
| `JamalPoolParty` | Jamal scene `JamalBilliardsSex` unlocked && `!isQuestActive("PoolParty")` && `day === "Friday"` && `getCorruptionLevel() ≥ 4` |
| `MarcusDate` | `Marcus.relation ≥ 15` && quest available && not already boyfriend → `startQuest` + `newMessage` |

`newMessage` creates the thread if absent, pushes the instanced message id, sets `hasUnread`, and fires a "You have a new message, check your phone!" notification. Separately, `QuestService.checkScheduledQuests()` decrements each quest's `delayDays` and auto-starts it at 0 (this is how `ScheduleQuest MarcusDate 15` re-fires).

**Doctrine:** the chat is the game's **time-driven, condition-gated quest-invitation / event bus.** The day tick delivers invites once relationship / corruption / day-of-week / scene-unlock conditions are satisfied.

---

## 6. Per-app reference

### 6.1 Instafame (`InstafameService`, `Instafame`, `Selfie`, `InstafameMessages`)
Fake Instagram. State: `{ account, name, followers, likes, selfieType, dm, posted }`. Account creation **is a quest reward** (`<<if isQuestActive("Instafame")>>` → "Create Instafame" button → `FinishQuest Instafame`).

**Posting** (`Selfie`): choose selfie / lewd (corr ≥ 3) / naked (corr ≥ 4) → random image → **Post**:

| Type | Followers gained | Gate |
|---|---|---|
| selfie | `random(5,20)` | — |
| lewd | `random(30,50)` | corr ≥ 3 |
| naked | `random(60,80)` | corr ≥ 4 |

`posted = true` after posting (daily cap, reset on the day cycle).

**DMs** (`InstafameMessages`) — appear conditionally in the Instafame view at **follower milestones** + quest progress (e.g. `followers ≥ 500 && getQuestProgress("BecomeAModel") == 0` → Richard). Each DM widget: `StartQuest` on view → scripted `<<Speech>>` → a `linkreplace` dialogue cascade → the **accept branch gated on corruption**; accept fires `UpdateQuest` + `UnlockLocation`; declining while too pure fires `<<NotifyCorruption N>>` (which surfaces the needed level to the player).

| DM | Corr gate | Quest | Pay / unlock |
|---|---|---|---|
| Jim | ≥ 4 | Pornstar | unlocks `filmStudio` |
| Richard | ≥ 2 | BecomeAModel | unlocks `photoStudio` |
| Richard (2nd) | ≥ 3 | SecondPhotoShoot | $150 |
| Edward | ≥ 3 | SecretAdmirer | $250, unlocks `hotel` |
| Edward (2nd) | ≥ 3 | SecondDate | $400 |
| Edward (3some) | ≥ 4 | Threesome | $600 |

The Edward arc is a single escalating client (virgin → repeat → threesome), pay laddering 250 → 400 → 600.

### 6.2 Naked Life (`NakedLifeService`, `NakedLife`)
Exhibitionist forum. State: `{ account, challenges[], rank, exp }`. Ranks at **XP thresholds 0 / 20 / 40 / 60** (Newbie / Exhibitionist / Shameless / Legend). XP gain per completed challenge by tier: **1 / 2 / 3 / 4**.

Each challenge = `{ id, title, description, rank, relatedScene, completed, active }` — e.g. Park Flash → `JoggingFlash`, Beach Flash → `SwimFlash`, Pool Flash → `PoolFlash`, Mall Flash → `MallFlash` (Newbie); Gym Flash → `GymFlash`, Restaurant Flash → `RestaurantFlash` (Exhibitionist); …

**Closed loop:** UI is a tabbed forum (by rank) with an XP-to-next-rank bar. **Accept** (`startNakedLifeChallenge`) checks `exp ≥ getXpThreshold(challenge.rank)`, then **`unlockChallengeLocation`** finds the location whose `passage === challenge.relatedScene` and sets `unlocked = true`, and marks the challenge `active`. Performing the world flash scene → `completeNakedLifeChallenge` → `+xp` → `rankUpByXp`. `isChallengeActive(scene)` gates the world scene to the active challenge.

### 6.3 Fast Jobs (`FastJobsService`, `FastJobs`)
Money grind. 4 jobs (`createJobs`):

| Job | Income | Day period | XP req |
|---|---|---|---|
| DogWalking | $45 | Afternoon | 0 |
| HouseCleaning | $75 | Morning | 5 |
| BabySitting | $110 | Afternoon | 10 |
| ElderlyCare | $110 | Morning | 10 |

Card gate states: `delayDays > 0` → "available again in N days" (**2-day cooldown** set on completion); `xp < required` → "need more XP"; else "Get Job". `startFastJob` requires `job.time === game().game.time` (period window) else a notification, then `enterLocation(job.name)`. The world scene → `finishFastJob`: `finished`, `delayDays = 2`, `fastJobs.xp += 1`, `addMoney(income)`. XP (only +1/job) is the ladder that unlocks higher-pay jobs.

### 6.4 PornCenter (`PornCenterService`, `PornCenter`) — built but **disabled**
The `PhoneHome` button is **commented out** (`/* … */`), so this app is dormant in the shipped build, but the code is live. State: `{ account, sites[] }`. 5 sites gated by **`player.corruption.points < site.corruption`** (note: corruption **points**, not level):

| Site | Genre | Corruption | 
|---|---|---|
| ZVideos | All | 5 |
| PornVub | All | 5 |
| Blackez | Interracial | 10 |
| FamilyLove | Taboo | 15 |
| F0rc3dWorld | Non-consent | 20 |

Watch only from the Bedroom → `PornCenterMasturbation`; `timesWatched++`.

### 6.5 Bank (`BankService`, `Bank` / `BankPhone`)
Savings account. Opened in-world (`openBankAccount` → `bank.open = true`); the phone app is gated `<<if $player.bank.open>>` else a "go to a bank" notification. `generateBankIncome` on the day tick = **1% daily interest** on positive balance. UI = balance + deposit/withdraw textbox.

### 6.6 xCam (`XCamService`, `xCam` on the Laptop)
Adult webcam platform. State: `{ account, name, exp, streamed }`. Create Account **double-gated**: `getCorruptionLevel() ≥ 4` **and** `isPurchased("webcam")`.

### 6.7 Utility apps
- **Quests** (`Quests`) → `<<ShowActiveQuests>>` journal; completed entries styled green.
- **Statistics** (`PlayerStats`) → read-only stat dump.

---

## 7. Daily-reset model

Three different reset idioms on the day tick:
- **Boolean reset** — `resetGameCycle` sets `instafame.posted = false` (re-enables daily posting).
- **Stat reset** — `resetPlayerStats`: `energy = maxEnergy`, `drunkness = 0`, `arousal += 1` (climbs, caps at `maxArousal = 10`), `makeup` cleared.
- **Self-expiring comparison** — the chat's `actionUsageDays[id]` is **never cleared**; it stores the day number and the gate checks `=== currentDay`. When `game().game.days` advances, the stored value no longer matches and the action re-enables automatically. (Elegant: no reset pass needed.)

---

## 8. Gallery mode

`galleryMode()` is an unlock-all browse mode. It **pins reads to maximum** — `getCorruptionLevel() → 4`, `getArousal() → 10`, `getExb() → 99`, `getQuestProgress() → 99` — and **skips mutators** (`FinishFastJob`, `AddTime`, `CompleteNakedLifeChallenge` early-return). Every corruption/arousal/quest gate in the phone passes automatically while it's on.

---

## 9. Unifying doctrine

The phone (with the laptop as its bedroom-bound sibling) is a **second hub**: the world map holds *in-person* activities, the devices package every *solo / remote* progression loop — money (Fast Jobs), fame (Instafame), exhibitionism (Naked Life), porn (PornCenter, dormant), camming (xCam), social/quests (Messages), banking, stats — as **isolated services with dumb views and a world-scene payback**. Every loop is paced by the same family of throttles:

- **corruption tier** (level for chat/Instafame/DMs; points for PornCenter)
- **daily cadence** (one selfie/lewd/nude per day; one post per day; per-action `actionUsageDays`; 2-day Fast Jobs cooldown)
- **XP / follower ladders** (Fast Jobs XP, Naked Life rank XP, Instafame follower milestones)
- **quest / account / hardware unlocks** (account creation as quest reward; phone $400 and webcam items)
- **day-tick dispatch** (invitations delivered when relationship / corruption / day-of-week / scene-unlock conditions hold)

---

## 10. Design philosophy

§9 captures the *structural* doctrine; this section extracts the *design intent*. Each principle in **10.1 is grounded in a concrete source anchor** (the philosophy the code demonstrably embodies). **10.2 lists reasonable inferences** — interpretation supported by those patterns but **not stated by the code**; treat them as lenses, not facts.

### 10.1 Evidenced design principles

1. **Earned, progressively-disclosed surface.** The phone is a $400 item (`isPurchased('phone')` gates the sidebar button); apps render conditionally in `PhoneHome` (`<<if instafame.account>>`, `<<if nakedLife.account>>`, `<<if bank.open>>`); the Instafame account is itself a quest reward (`<<if isQuestActive("Instafame")>>` → `<<FinishQuest Instafame>>`). → *The phone and each app are unlocked through play, not handed over at start.*
2. **The phone dispatches; the world resolves.** Every app loop closes through a world scene that calls back: `FinishQuest`×29, `FinishFastJob`×9, `AddInstafameFollowers`×3; Naked Life's `unlockChallengeLocation` → world flash scene → `completeNakedLifeChallenge`. → *Apps are set-up/tracking surfaces; content and payoff live in world scenes — the phone never resolves a scene itself.*
3. **Gates are telegraphed, not hidden.** Dedicated macros exist solely to announce the requirement when content is locked: `NotifyCorruption` → *"You are not corrupted enough to do this. (N+ corruption required!)"* (`pointsMap = [0,5,15,30,45]`), and `StageNotification` → *"You need to corrupt your [relationship] more! They need at least 5 corruption and to be a little aroused 🔥!"*. → *Locked content shows itself and states its threshold, turning every gate into a visible goal.*
4. **Stacked, orthogonal gating.** The same content is gated on several independent axes at once: hardware purchase (phone/webcam items) + account/quest unlock + corruption tier (level→points map) + daily cadence + XP/follower/rank ladders. → *Money, narrative, corruption, time, and skill each gate in parallel.*
5. **Corruption is the escalation spine of every app.** `sendLewd≥3`/`sendNude≥4`; lewd selfie ≥3 / naked ≥4; PornCenter genres at corruption 5/10/15/20; DM accepts gated by level. → *One global corruption stat is the master key that escalates content uniformly across all apps.*
6. **Daily cadence is the universal throttle.** `actionUsageDays===currentDay` (chat), `instafame.posted` daily reset, Fast Jobs `delayDays=2`, daily chat `count<1`. → *Almost every repeatable action is capped per-day (or per-N-days).*
7. **The phone reacts to world state.** `newMessage` dispatched on the day tick gated by `relation≥15` / `corruption≥4` / `day==='Friday'` / scene-unlocked; DMs appear at follower milestones (≥500). → *Content surfaces in response to progress made elsewhere (relationships, corruption, fame).*
8. **Service-isolated modularity.** Each app is its own Service class; passages are dumb views; the phone is a container. → *Apps are independent modules behind a shared shell — addable/removable without coupling.*
9. **Device placement by context.** Phone (sidebar, everywhere) vs Laptop (bedroom-only: Watch Porn, xCam). → *Device = where the activity plausibly happens — mobile vs home.*
10. **Social apps are escalating monetized funnels.** DMs start quests and ladder pay (Edward 250→400→600), each gated higher on corruption. → *Visibility/fame → inbound offers → escalating transactional content.*

### 10.2 Reasonable inferences (interpretation — NOT stated by the source)

Supported by the patterns above but not demonstrated by the code; do not cite as fact:
- Daily caps exist **to pace consumption to the sleep/day loop and prevent bingeing** (inferred from the consistent throttle pattern, principle 6).
- The phone **answers "what do I do now?" between in-person scenes / makes downtime productive** (inferred from the second-hub structure).
- The app metaphor is **a diegetic wrapper to make grinds feel natural** (the metaphor is real; the *intent* is interpretation).
- The phone is **a player-initiated corruption-expression surface** (that the player initiates posts/sends/swipes is evidenced; the psychological framing is interpretation).

---

*Source of record: `game_explorations/road-to-success/_storyjs_dump.js` (modules #40 PhoneController, #66 phone.model, #98 xCamService, #99 PhoneService, #100 FastJobsService, #101 InstafameService, #102 NakedLifeService, #103 PornCenterService, #104 TimeService) + `passage_catalog.json` (Phone, PhoneHome, PhoneTop, Messages, PhoneMessages, Instafame, Selfie, InstafameDM, InstafameMessages, NakedLife, FastJobs, PornCenter, Bank, Laptop, xCam, Quests) + explorer `notes.md`. No TLS design implied — analysis only.*
