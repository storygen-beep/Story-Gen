# zaras-school-life — Exploration Report

Generated: 2026-04-16T18:07:18.872Z
Source URL: https://mopoga.com/zaras-school-life

## Session Summary

- Sessions run: 2
- Total wall-clock: 135m 43s
- Total clicks: 140
- Total choices explored: 140
- Unique states seen: 140
- Unexplored frontier (queued for next session): 0
- Any ending reached: not yet

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `jessica.reputation` | number | 100..100 | 0 | high |
| `janet.willpower` | number | 0..0 | 0 | high |

### npc_stat (6)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `PlayerCorruption` | number | 0..35 | 5 | high |
| `dad.corruption` | number | 0..1 | 1 | high |
| `bro.corruption` | number | 0..50 | 1 | high |
| `mom.corruption` | number | 0..1 | 1 | high |
| `bro.love` | number | 50..50 | 0 | high |
| `bro.lust` | number | 50..50 | 0 | high |

### time (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `hour` | number | 8..22 | 12 | high |
| `day` | number | 1..4 | 2 | high |

### flag (155)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `startUpOnce` | boolean | true | 0 | high |
| `PlayerOneQuestDone` | boolean | false, true | 1 | high |
| `mgSkipSpeech` | boolean | false | 0 | high |
| `mgSkipHack` | boolean | false | 0 | high |
| `mgSkipStruggle` | boolean | false | 0 | high |
| `mgSkipTiming` | boolean | false | 0 | high |
| `studiousGirl` | boolean | false | 0 | high |
| `fitGirl` | boolean | false | 0 | high |
| `redPrices` | boolean | false | 0 | high |
| `PlayerShower` | boolean | false, true | 2 | high |
| `PlayerGymAttire` | boolean | true | 0 | high |
| `PlayerGymAdv` | boolean | false | 0 | high |
| `PlayerSwimWear` | boolean | false | 0 | high |
| `PlayerSchoolUniSlutty` | boolean | false | 0 | high |
| `PlayerSluttyClothes` | boolean | false | 0 | high |
| `PlayerCam` | boolean | false, true | 1 | high |
| `PlayerTab` | boolean | false, true | 1 | high |
| `PlayerPhone` | boolean | false, true | 1 | high |
| `PlayerDildo` | boolean | false, true | 1 | high |
| `PlayerStrapon` | boolean | false | 0 | high |
| `camming` | boolean | false | 0 | high |
| `dailyHangDick` | boolean | false | 0 | high |
| `dailyHangBen` | boolean | false | 0 | high |
| `dailyHangJason` | boolean | false | 0 | high |
| `dailyHangLisa` | boolean | false | 0 | high |
| `dailyHangBro` | boolean | false, true | 2 | high |
| `dailyHangDad` | boolean | false | 0 | high |
| `dailyHangMom` | boolean | false | 0 | high |
| `dailyHangDaniel` | boolean | false | 0 | high |
| `weeklyAllowanceCheck` | boolean | false | 0 | high |
| `dailyChores` | boolean | false | 0 | high |
| `stayOut` | boolean | false | 0 | high |
| `curfewCheck` | boolean | false | 0 | high |
| `detentionFlag` | boolean | false | 0 | high |
| `CDstart` | boolean | false | 0 | high |
| `CDstop` | boolean | false | 0 | high |
| `famSexUnlocked` | boolean | false, true | 1 | high |
| `dad.isTakingShower` | boolean | false | 0 | high |
| `dad.blowjob` | boolean | false | 0 | high |
| `dad.sex` | boolean | false | 0 | high |
| … | … | … | … | and 115 more |

### scalar (96)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `version` | number | 2..2 | 0 | low |
| `PlayerMoney` | number | 0..1000 | 2 | low |
| `PlayerEnergy` | number | 20..110 | 10 | low |
| `PlayerMaxEnergy` | number | 100..110 | 2 | low |
| `PlayerSchoolRep` | number | 0..15 | 2 | low |
| `PlayerFitness` | number | 0..10 | 2 | low |
| `PlayerActiveQuest` | number | 0..1 | 2 | low |
| `PlayerArt` | number | 0..2 | 1 | low |
| `PlayerSci` | number | 0..0 | 0 | low |
| `PlayerComp` | number | 0..2 | 1 | low |
| `playerActiveQuests` | number | 0..1 | 4 | low |
| `playerGymSub` | number | 0..0 | 0 | low |
| `PlayerGroceries` | number | 5..5 | 0 | low |
| `PlayerSnacks` | number | 5..5 | 0 | low |
| `zararejectDay` | number | 0..0 | 0 | low |
| `lastDayBreakfast` | number | 0..0 | 0 | low |
| `lastDayLunch` | number | 0..0 | 0 | low |
| `lastDayDinner` | number | 0..0 | 0 | low |
| `lastDayDrawing` | number | 0..0 | 0 | low |
| `punishTimes` | number | 0..0 | 0 | low |
| `allowanceTimes` | number | 0..0 | 0 | low |
| `watchTVtimes` | number | 0..0 | 0 | low |
| `dailyText` | number | 0..0 | 0 | low |
| `drawFans` | number | 0..0 | 0 | low |
| `camFans` | number | 0..0 | 0 | low |
| `choresCount` | number | 0..0 | 0 | low |
| `classAttended` | number | 0..4 | 2 | low |
| `classNAttended` | number | 0..0 | 0 | low |
| `drugStatus` | number | 0..0 | 0 | low |
| `drugPackets` | number | 0..0 | 0 | low |
| `drugIngredients` | number | 0..0 | 0 | low |
| `minute` | number | 0..57 | 48 | low |
| `dayCount` | number | 1..4 | 2 | low |
| `dateDay` | number | 1..4 | 2 | low |
| `dad.dailyVisits` | number | 0..0 | 0 | low |
| `dad.rejectDay` | number | 0..0 | 0 | low |
| `dad.activeQuest` | number | 0..0 | 0 | low |
| `dad.lastQuest` | number | 0..0 | 0 | low |
| `bro.dailyVisits` | number | 0..3 | 5 | low |
| `bro.rejectDay` | number | 0..4 | 1 | low |
| … | … | … | … | and 56 more |

### string (34)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `PlayerClothes` | string | `Casual` | 0 | low |
| `drugStatusAlt` | string | `F` | 0 | low |
| `dayOfWeek` | string | `Monday`, `Wednesday`, `Saturday` | 3 | low |
| `dateMonth` | string | `March` | 0 | low |
| `dad.name` | string | `Ben` | 0 | low |
| `dad.lname` | string | `Williams` | 0 | low |
| `dad.currentLocation` | string | `` | 0 | low |
| `dad.activity` | string | `` | 0 | low |
| `bro.name` | string | `Kyle` | 0 | low |
| `bro.lname` | string | `Williams` | 0 | low |
| `bro.currentLocation` | string | `` | 0 | low |
| `bro.activity` | string | `` | 0 | low |
| `mom.name` | string | `Elena` | 0 | low |
| `mom.lname` | string | `Williams` | 0 | low |
| `mom.currentLocation` | string | `` | 0 | low |
| `mom.activity` | string | `` | 0 | low |
| `dick.name` | string | `Dick` | 0 | low |
| `dick.lname` | string | `Turpin` | 0 | low |
| `ben.name` | string | `Ben` | 0 | low |
| `ben.lname` | string | `Kingsley` | 0 | low |
| `jason.name` | string | `Jason` | 0 | low |
| `jason.lname` | string | `Quill` | 0 | low |
| `daniel.name` | string | `Daniel` | 0 | low |
| `daniel.lname` | string | `Miller` | 0 | low |
| `lisa.name` | string | `Lisa` | 0 | low |
| `lisa.lname` | string | `Brown` | 0 | low |
| `jessica.name` | string | `Jessica` | 0 | low |
| `jessica.lname` | string | `Chambers` | 0 | low |
| `janet.name` | string | `Janet` | 0 | low |
| `janet.lname` | string | `Smith` | 0 | low |
| `return` | string | `Welcome Page`, `Jecinda District`, `travel walk event3` | 53 | low |
| `timeOfDay` | string | `Day`, `Night` | 5 | low |
| `walkLocation` | string | `Arabella` | 0 | low |
| `hangLoc` | string | `park` | 0 | low |

### misc (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `commissions` | object | — | 0 | low |
| `minutes` | object | — | 0 | low |

## NPCs detected

| npc | stats observed | var count |
|---|---|---|
| player | corruption | 1 |
| dad | corruption | 1 |
| bro | corruption, love, lust | 3 |
| mom | corruption | 1 |

## Body / appearance traits

_No body/appearance variables detected._

## Choice type distribution

| type | count |
|---|---|
| branch | 61 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 0
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **name** (10): `dad.name`, `bro.name`, `mom.name`, `dick.name`, `ben.name`, `jason.name`, …
- **lname** (10): `dad.lname`, `bro.lname`, `mom.lname`, `dick.lname`, `ben.lname`, `jason.lname`, …
- **dailyvisits** (10): `dad.dailyVisits`, `bro.dailyVisits`, `mom.dailyVisits`, `dick.dailyVisits`, `ben.dailyVisits`, `jason.dailyVisits`, …
- **rejectday** (10): `dad.rejectDay`, `bro.rejectDay`, `mom.rejectDay`, `dick.rejectDay`, `ben.rejectDay`, `jason.rejectDay`, …
- **angryflag** (10): `dad.angryFlag`, `bro.angryFlag`, `mom.angryFlag`, `dick.angryFlag`, `ben.angryFlag`, `jason.angryFlag`, …
- **activequest** (10): `dad.activeQuest`, `bro.activeQuest`, `mom.activeQuest`, `dick.activeQuest`, `ben.activeQuest`, `jason.activeQuest`, …
- **lastquest** (10): `dad.lastQuest`, `bro.lastQuest`, `mom.lastQuest`, `dick.lastQuest`, `ben.lastQuest`, `jason.lastQuest`, …
- **relationship** (8): `dick.relationship`, `ben.relationship`, `jason.relationship`, `daniel.relationship`, `lisa.relationship`, `jessica.relationship`, …
- **metflag** (7): `dick.metFlag`, `ben.metFlag`, `jason.metFlag`, `daniel.metFlag`, `lisa.metFlag`, `jessica.metFlag`, …
- **datingflag** (7): `dick.datingFlag`, `ben.datingFlag`, `jason.datingFlag`, `daniel.datingFlag`, `lisa.datingFlag`, `jessica.datingFlag`, …
- **datingq** (7): `dick.datingQ`, `ben.datingQ`, `jason.datingQ`, `daniel.datingQ`, `lisa.datingQ`, `jessica.datingQ`, …
- **wentdate** (7): `dick.wentDate`, `ben.wentDate`, `jason.wentDate`, `daniel.wentDate`, `lisa.wentDate`, `jessica.wentDate`, …
- **totaldates** (7): `dick.totalDates`, `ben.totalDates`, `jason.totalDates`, `daniel.totalDates`, `lisa.totalDates`, `jessica.totalDates`, …
- **school** (6): `school2ndDayEventFlash`, `school3rdDayEventGroped`, `school1stDayEvent`, `school2ndDayEvent`, `school2ndDayEventOffer`, `school3rdDayEvent`
- **blowjob** (5): `dad.blowjob`, `bro.blowjob`, `ben.blowjob`, `jason.blowjob`, `daniel.blowjob`
- **sex** (5): `dad.sex`, `bro.sex`, `ben.sex`, `jason.sex`, `daniel.sex`
- **anal** (5): `dad.anal`, `bro.anal`, `ben.anal`, `jason.anal`, `daniel.anal`
- **dick** (4): `dick2aBossDead`, `dick2aBossRape`, `dick2aSex`, `dick2bBB`
- **corruption** (3): `dad.corruption`, `bro.corruption`, `mom.corruption`
- **currentlocation** (3): `dad.currentLocation`, `bro.currentLocation`, `mom.currentLocation`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-16T15:50:44.762Z | 109m 55s | 79 | 79 | 79 | no |
| 2 | 2026-04-16T17:41:30.486Z | 25m 48s | 61 | 61 | 61 | no |

## See also
- `variable_profile.json` — raw statistical evidence, no labels
- `variable_schema.json` — variables with applied labels + confidence
- `mechanics.md` — design patterns observed
- `coverage.md` — frontier + explored counts
- `choice_graph.json` — decision graph
- `state_timeline.jsonl` — per-click state snapshots