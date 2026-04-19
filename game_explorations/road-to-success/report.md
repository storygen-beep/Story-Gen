# road-to-success — Exploration Report

Generated: 2026-04-19T10:44:13.636Z
Source URL: https://mopoga.com/road-to-success

## Session Summary

- Sessions run: 6
- Total wall-clock: 89m 8s
- Total clicks: 106
- Total choices explored: 106
- Unique states seen: 373
- Unexplored frontier (queued for next session): 0
- Endings reached: 0 (use `live.js mark-ending <passage>` to record a terminal passage)

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (139)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `player.energy` | number | 100..100 | 0 | high |
| `player.money` | number | 50..5019 | 3 | high |
| `player.intelligence` | number | 0..21 | 2 | high |
| `player.fitness` | number | 0..10 | 1 | high |
| `player.beauty` | number | 0..0 | 0 | high |
| `player.clothing.beauty` | number | 0..0 | 0 | high |
| `player.clothing.corruption` | number | 0..0 | 0 | high |
| `player.lastClothing.beauty` | number | 0..0 | 0 | high |
| `player.lastClothing.corruption` | number | 0..0 | 0 | high |
| `player.scenes.XCam.requirementsMC.corruption` | number | 45..45 | 0 | high |
| `player.scenes.BathroomLactation.requirementsMC.corruption` | number | 0..0 | 0 | high |
| `player.scenes.XCamBlackmail.requirementsMC.corruption` | number | 0..0 | 0 | high |
| `player.scenes.HouseCleaning1.requirementsMC.corruption` | number | 30..30 | 0 | high |
| `player.scenes.DogWalking.requirementsMC.corruption` | number | 30..30 | 0 | high |
| `player.scenes.BabySitting.requirementsMC.corruption` | number | 30..30 | 0 | high |
| `player.scenes.ElderlyCare.requirementsMC.corruption` | number | 30..30 | 0 | high |
| `player.scenes.BedroomMasturbate1.requirementsMC.corruption` | number | 0..0 | 0 | high |
| `player.scenes.HouseCleaning2.requirementsMC.corruption` | number | 30..30 | 0 | high |
| `player.scenes.xCamPizzaDelivery.requirementsMC.corruption` | number | 45..45 | 0 | high |
| `player.scenes.SchoolBathroomMasturbate.requirementsMC.corruption` | number | 0..0 | 0 | high |
| `player.drugs.modifiers.energy` | number | -10..0 | 1 | high |
| `player.drugs.modifiers.intelligence` | number | -5..0 | 1 | high |
| `player.drugs.modifiers.fitness` | number | -5..0 | 1 | high |
| `player.drugs.modifiers.beauty` | number | -3..0 | 1 | high |
| `npc.Dad.corruption` | number | 0..0 | 0 | high |
| `npc.Brother.corruption` | number | 0..0 | 0 | high |
| `npc.Grandpa.corruption` | number | 0..0 | 0 | high |
| `npc.Marcus.corruption` | number | 0..0 | 0 | high |
| `npc.Sam.corruption` | number | 0..0 | 0 | high |
| `npc.Oliver.corruption` | number | 0..0 | 0 | high |
| `npc.Janitor.corruption` | number | 0..0 | 0 | high |
| `npc.MathTeacher.corruption` | number | 0..0 | 0 | high |
| `npc.Coach.corruption` | number | 0..0 | 0 | high |
| `npc.Natasha.corruption` | number | 0..0 | 0 | high |
| `npc.Emma.corruption` | number | 0..0 | 0 | high |
| `npc.ComputerTeacher.corruption` | number | 0..0 | 0 | high |
| `npc.Thomas.corruption` | number | 0..0 | 0 | high |
| `npc.Strange.corruption` | number | 0..0 | 0 | high |
| `npc.StrangeBBC.corruption` | number | 0..0 | 0 | high |
| `npc.Maya.corruption` | number | 0..0 | 0 | high |
| … | … | … | … | and 99 more |

### npc_stat (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `game.maxArousal` | number | 10..10 | 0 | high |
| `player.drugs.drugAddiction` | number | 0..35 | 1 | high |

### body (7)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `game.preferences.pregnancyDays` | number | 21..21 | 0 | medium |
| `game.preferences.pregnancyChance` | number | 33..33 | 0 | medium |
| `player.makeup` | number | 0..0 | 0 | medium |
| `player.inventory.pregnancyTest` | number | 0..0 | 0 | medium |
| `player.statistics.miscarriages` | number | 0..0 | 0 | medium |
| `player.statistics.pregnancies` | number | 0..0 | 0 | medium |
| `clothingStoreCategory` | string | `casual` | 0 | medium |

### time (9)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `%%cycles.time` | object | — | 0 | high |
| `%%cycles.day` | object | — | 0 | high |
| `game.time` | string | `EM`, `M` | 1 | high |
| `game.day` | string | `Monday`, `Wednesday` | 1 | high |
| `location.school.MathClass.time` | string | `EM` | 0 | high |
| `location.school.HistoryClass.time` | string | `M` | 0 | high |
| `location.school.ComputerClass.time` | string | `M` | 0 | high |
| `location.school.PEClass.time` | string | `A` | 0 | high |
| `location.school.EmptyClass.time` | string | `E` | 0 | high |

### item (55)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `properties.apartment.hasLateFee` | boolean | false | 0 | high |
| `player.inventory.weed` | number | 0..4 | 1 | medium |
| `npc.Dad.key` | string | `Dad` | 0 | medium |
| `npc.Brother.key` | string | `Brother` | 0 | medium |
| `npc.Grandpa.key` | string | `Grandpa` | 0 | medium |
| `npc.Marcus.key` | string | `Marcus` | 0 | medium |
| `npc.Sam.key` | string | `Sam` | 0 | medium |
| `npc.Oliver.key` | string | `Oliver` | 0 | medium |
| `npc.Janitor.key` | string | `Janitor` | 0 | medium |
| `npc.MathTeacher.key` | string | `MathTeacher` | 0 | medium |
| `npc.Coach.key` | string | `Coach` | 0 | medium |
| `npc.Natasha.key` | string | `Natasha` | 0 | medium |
| `npc.Emma.key` | string | `Emma` | 0 | medium |
| `npc.ComputerTeacher.key` | string | `ComputerTeacher` | 0 | medium |
| `npc.Thomas.key` | string | `Thomas` | 0 | medium |
| `npc.Strange.key` | string | `Strange` | 0 | medium |
| `npc.StrangeBBC.key` | string | `StrangeBBC` | 0 | medium |
| `npc.Maya.key` | string | `Maya` | 0 | medium |
| `npc.Jim.key` | string | `Jim` | 0 | medium |
| `npc.Richard.key` | string | `Richard` | 0 | medium |
| `npc.Boss.key` | string | `Boss` | 0 | medium |
| `npc.Michael.key` | string | `Michael` | 0 | medium |
| `npc.Susan.key` | string | `Susan` | 0 | medium |
| `npc.OfficeBoss.key` | string | `OfficeBoss` | 0 | medium |
| `npc.Jamal.key` | string | `Jamal` | 0 | medium |
| `npc.ClubBouncer.key` | string | `ClubBouncer` | 0 | medium |
| `npc.Veronica.key` | string | `Veronica` | 0 | medium |
| `npc.PersonalTrainer.key` | string | `PersonalTrainer` | 0 | medium |
| `npc.Priest.key` | string | `Priest` | 0 | medium |
| `npc.Gangster.key` | string | `Gangster` | 0 | medium |
| `npc.DrugDealer.key` | string | `DrugDealer` | 0 | medium |
| `npc.KingCobra.key` | string | `KingCobra` | 0 | medium |
| `npc.Mamba.key` | string | `Mamba` | 0 | medium |
| `npc.Krait.key` | string | `Krait` | 0 | medium |
| `npc.StripClubManager.key` | string | `StripClubManager` | 0 | medium |
| `npc.Stripper.key` | string | `Stripper` | 0 | medium |
| `npc.Bartender.key` | string | `Bartender` | 0 | medium |
| `npc.Matthew.key` | string | `Matthew` | 0 | medium |
| `npc.PoliceMan.key` | string | `PoliceMan` | 0 | medium |
| `npc.PoliceWoman.key` | string | `PoliceWoman` | 0 | medium |
| … | … | … | … | and 15 more |

### flag (1521)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `dev.devMode` | boolean | false | 0 | high |
| `dev.gUn` | boolean | false | 0 | high |
| `dev.uAs` | boolean | false | 0 | high |
| `dev.galleryMode` | boolean | false | 0 | high |
| `game.intro` | boolean | true, false | 1 | high |
| `game.preferences.changeClothesAuto` | boolean | false | 0 | high |
| `game.preferences.autoplayVideos` | boolean | false | 0 | high |
| `game.preferences.muteVideos` | boolean | false | 0 | high |
| `game.preferences.loopVideos` | boolean | true | 0 | high |
| `game.preferences.autoSave` | boolean | false | 0 | high |
| `location.center.open` | boolean | true | 0 | high |
| `location.center.unlocked` | boolean | true | 0 | high |
| `location.center.scenes.StreetChallenge1.unlocked` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.executedToday` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.gallery` | boolean | true | 0 | high |
| `location.center.scenes.StreetChallenge1.inside` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.blowjob` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.vaginal` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.anal` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.threesome` | boolean | false | 0 | high |
| `location.center.scenes.StreetChallenge1.gangbang` | boolean | false | 0 | high |
| `location.residential.open` | boolean | true | 0 | high |
| `location.residential.unlocked` | boolean | true | 0 | high |
| `location.elite.open` | boolean | true | 0 | high |
| `location.elite.unlocked` | boolean | true | 0 | high |
| `location.ghetto.open` | boolean | true | 0 | high |
| `location.ghetto.unlocked` | boolean | true | 0 | high |
| `location.house.open` | boolean | true | 0 | high |
| `location.house.unlocked` | boolean | true | 0 | high |
| `location.house.scenes.PizzaDelivery.unlocked` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.executedToday` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.gallery` | boolean | true | 0 | high |
| `location.house.scenes.PizzaDelivery.inside` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.blowjob` | boolean | true | 0 | high |
| `location.house.scenes.PizzaDelivery.vaginal` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.anal` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.threesome` | boolean | false | 0 | high |
| `location.house.scenes.PizzaDelivery.gangbang` | boolean | false | 0 | high |
| `location.busStop.open` | boolean | true | 0 | high |
| `location.busStop.unlocked` | boolean | true | 0 | high |
| … | … | … | … | and 1481 more |

### scalar (584)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `game.days` | number | 1..3 | 1 | low |
| `game.dice` | number | 0..1 | 1 | low |
| `game.randomMoney` | number | 0..19 | 1 | low |
| `game.maxEnergy` | number | 100..100 | 0 | low |
| `game.questStartCounter` | number | 0..7 | 2 | low |
| `game.preferences.autoSaveSlot` | number | 0..0 | 0 | low |
| `game.random` | number | 2..30 | 50 | low |
| `items.laptop.price` | number | 800..800 | 0 | low |
| `items.phone.price` | number | 400..400 | 0 | low |
| `items.webcam.price` | number | 200..200 | 0 | low |
| `items.oneDayGym.price` | number | 40..40 | 0 | low |
| `items.sevenDayGym.price` | number | 120..120 | 0 | low |
| `items.thirtyDayGym.price` | number | 250..250 | 0 | low |
| `items.lifetimegym.price` | number | 1100..1100 | 0 | low |
| `items.pregnancyTest.price` | number | 12..12 | 0 | low |
| `items.contraceptivePill.price` | number | 8..8 | 0 | low |
| `items.weed.price` | number | 18..18 | 0 | low |
| `items.cocaine.price` | number | 90..90 | 0 | low |
| `items.heroin.price` | number | 170..170 | 0 | low |
| `items.fakeID.price` | number | 150..150 | 0 | low |
| `properties.apartment.price` | number | 300..300 | 0 | low |
| `properties.apartment.rentCycleDays` | number | 7..7 | 0 | low |
| `properties.apartment.daysUntilRent` | number | 7..7 | 0 | low |
| `properties.apartment.accumulatedDebt` | number | 0..0 | 0 | low |
| `properties.apartment.skippedRentCount` | number | 0..0 | 0 | low |
| `location.center.scenes.StreetChallenge1.id` | number | 60..60 | 0 | low |
| `location.center.scenes.StreetChallenge1.chance` | number | 100..100 | 0 | low |
| `location.house.scenes.PizzaDelivery.id` | number | 1..1 | 0 | low |
| `location.house.scenes.PizzaDelivery.chance` | number | 33..33 | 0 | low |
| `location.bus.scenes.BusFlash.id` | number | 42..42 | 0 | low |
| `location.bus.scenes.BusFlash.chance` | number | 50..50 | 0 | low |
| `location.bus.scenes.BusMasturbate.id` | number | 43..43 | 0 | low |
| `location.bus.scenes.BusMasturbate.chance` | number | 33..33 | 0 | low |
| `location.bus.scenes.BusGrope.id` | number | 44..44 | 0 | low |
| `location.bus.scenes.BusGrope.chance` | number | 33..33 | 0 | low |
| `location.photoStudio.scenes.ModelPhotoshoot.id` | number | 38..38 | 0 | low |
| `location.photoStudio.scenes.ModelPhotoshoot.chance` | number | 100..100 | 0 | low |
| `location.photoStudio.scenes.SecondPhotoShoot.id` | number | 56..56 | 0 | low |
| `location.photoStudio.scenes.SecondPhotoShoot.chance` | number | 100..100 | 0 | low |
| `location.school.daysToNextTest` | number | 0..7 | 1 | low |
| … | … | … | … | and 544 more |

### string (991)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `dev.ptPw` | string | `d9f9133fb120cd609687` | 0 | low |
| `dev.gPW` | string | `eb31c3dfedd8947dfc4a` | 0 | low |
| `dev.galleryCode` | string | `` | 0 | low |
| `game.randomMedia` | string | ``, `drink2.webp`, `flash8.webp` | 4 | low |
| `game.timeIcon` | string | `🌤️`, `☀️` | 1 | low |
| `game.weather` | string | `clear`, `rain` | 1 | low |
| `game.weatherIcon` | string | `☀️`, `🌧️` | 1 | low |
| `game.lastPassage` | string | ``, `ConfessionSex`, `HospitalBirth` | 49 | low |
| `game.saveVersion` | string | `0.24` | 0 | low |
| `game.version` | string | `0.24` | 0 | low |
| `game.activeWardrobeTab` | string | `Casual`, `school` | 1 | low |
| `game.pinnedQuestKey` | string | `` | 0 | low |
| `items.laptop.name` | string | `laptop` | 0 | low |
| `items.laptop.title` | string | `Laptop` | 0 | low |
| `items.laptop.image` | string | `laptop.webp` | 0 | low |
| `items.laptop.type` | string | `electronics` | 0 | low |
| `items.laptop.icon` | string | `💻` | 0 | low |
| `items.phone.name` | string | `phone` | 0 | low |
| `items.phone.title` | string | `Phone` | 0 | low |
| `items.phone.image` | string | `phone.webp` | 0 | low |
| `items.phone.type` | string | `electronics` | 0 | low |
| `items.phone.icon` | string | `📱` | 0 | low |
| `items.webcam.name` | string | `webcam` | 0 | low |
| `items.webcam.title` | string | `Webcam` | 0 | low |
| `items.webcam.image` | string | `webcam.webp` | 0 | low |
| `items.webcam.type` | string | `electronics` | 0 | low |
| `items.webcam.icon` | string | `📷` | 0 | low |
| `items.oneDayGym.name` | string | `oneDayGym` | 0 | low |
| `items.oneDayGym.title` | string | `1 Day Membership` | 0 | low |
| `items.oneDayGym.image` | string | `1daybanner.webp` | 0 | low |
| `items.oneDayGym.type` | string | `gym` | 0 | low |
| `items.oneDayGym.icon` | string | `🏋️` | 0 | low |
| `items.sevenDayGym.name` | string | `sevenDayGym` | 0 | low |
| `items.sevenDayGym.title` | string | `7 Days Membership` | 0 | low |
| `items.sevenDayGym.image` | string | `7daybanner.webp` | 0 | low |
| `items.sevenDayGym.type` | string | `gym` | 0 | low |
| `items.sevenDayGym.icon` | string | `🧘` | 0 | low |
| `items.thirtyDayGym.name` | string | `thirtyDayGym` | 0 | low |
| `items.thirtyDayGym.title` | string | `30 Days Membership` | 0 | low |
| `items.thirtyDayGym.image` | string | `30daybanner.webp` | 0 | low |
| … | … | … | … | and 951 more |

### misc (34)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `location.photoStudio.openPeriods` | object | — | 0 | low |
| `location.school.testsHistory` | object | — | 0 | low |
| `location.school.openPeriods` | object | — | 0 | low |
| `location.park.openPeriods` | object | — | 0 | low |
| `location.marcusHouse.openPeriods` | object | — | 0 | low |
| `location.emmaHouse.openPeriods` | object | — | 0 | low |
| `location.gym.openPeriods` | object | — | 0 | low |
| `location.mall.openPeriods` | object | — | 0 | low |
| `location.club.openPeriods` | object | — | 0 | low |
| `location.beach.openPeriods` | object | — | 0 | low |
| `location.bar.openPeriods` | object | — | 0 | low |
| `location.pool.openPeriods` | object | — | 0 | low |
| `location.office.openPeriods` | object | — | 0 | low |
| `location.bank.openPeriods` | object | — | 0 | low |
| `location.drivingSchool.openPeriods` | object | — | 0 | low |
| `location.jamalHouse.openPeriods` | object | — | 0 | low |
| `location.veronicaHouse.openPeriods` | object | — | 0 | low |
| `location.thomasHouse.openPeriods` | object | — | 0 | low |
| `location.church.openPeriods` | object | — | 0 | low |
| `location.stripclub.openPeriods` | object | — | 0 | low |
| `location.clandestineClinic.openPeriods` | object | — | 0 | low |
| `location.restaurant.openPeriods` | object | — | 0 | low |
| `location.hospital.sperm` | object | — | 0 | low |
| `location.laundry.openPeriods` | object | — | 0 | low |
| `location.Casino.openPeriods` | object | — | 0 | low |
| `location.movieTheater.openPeriods` | object | — | 0 | low |
| `player.phone.threads` | object | — | 0 | low |
| `player.phone.nakedLife.challenges` | object | — | 0 | low |
| `player.phone.pornCenter.sites` | object | — | 0 | low |
| `player.baby` | object | — | 0 | low |
| `player.jobs` | object | — | 0 | low |
| `player.residence.ownedProperties` | object | — | 0 | low |
| `player.residence.rentedProperties` | object | — | 0 | low |
| `questList` | object | — | 0 | low |

## NPCs detected

| npc | stats observed | var count |
|---|---|---|
| max | arousal | 1 |
| drug | addiction | 1 |

## Body / appearance traits

- `game.preferences.pregnancyDays`
- `game.preferences.pregnancyChance`
- `player.makeup`
- `player.inventory.pregnancyTest`
- `player.statistics.miscarriages`
- `player.statistics.pregnancies`
- `clothingStoreCategory`


## Choice type distribution

| type | count |
|---|---|
| branch | 3 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 3
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **title** (238): `items.laptop.title`, `items.phone.title`, `items.webcam.title`, `items.oneDayGym.title`, `items.sevenDayGym.title`, `items.thirtyDayGym.title`, …
- **id** (196): `properties.apartment.id`, `location.center.scenes.StreetChallenge1.id`, `location.house.scenes.PizzaDelivery.id`, `location.bus.scenes.BusFlash.id`, `location.bus.scenes.BusMasturbate.id`, `location.bus.scenes.BusGrope.id`, …
- **unlocked** (186): `location.center.unlocked`, `location.center.scenes.StreetChallenge1.unlocked`, `location.residential.unlocked`, `location.elite.unlocked`, `location.ghetto.unlocked`, `location.house.unlocked`, …
- **name** (147): `items.laptop.name`, `items.phone.name`, `items.webcam.name`, `items.oneDayGym.name`, `items.sevenDayGym.name`, `items.thirtyDayGym.name`, …
- **vaginal** (143): `location.center.scenes.StreetChallenge1.vaginal`, `location.house.scenes.PizzaDelivery.vaginal`, `location.bus.scenes.BusFlash.vaginal`, `location.bus.scenes.BusMasturbate.vaginal`, `location.bus.scenes.BusGrope.vaginal`, `location.photoStudio.scenes.ModelPhotoshoot.vaginal`, …
- **anal** (143): `location.center.scenes.StreetChallenge1.anal`, `location.house.scenes.PizzaDelivery.anal`, `location.bus.scenes.BusFlash.anal`, `location.bus.scenes.BusMasturbate.anal`, `location.bus.scenes.BusGrope.anal`, `location.photoStudio.scenes.ModelPhotoshoot.anal`, …
- **chance** (142): `location.center.scenes.StreetChallenge1.chance`, `location.house.scenes.PizzaDelivery.chance`, `location.bus.scenes.BusFlash.chance`, `location.bus.scenes.BusMasturbate.chance`, `location.bus.scenes.BusGrope.chance`, `location.photoStudio.scenes.ModelPhotoshoot.chance`, …
- **guide** (142): `location.center.scenes.StreetChallenge1.guide`, `location.house.scenes.PizzaDelivery.guide`, `location.bus.scenes.BusFlash.guide`, `location.bus.scenes.BusMasturbate.guide`, `location.bus.scenes.BusGrope.guide`, `location.photoStudio.scenes.ModelPhotoshoot.guide`, …
- **executedtoday** (142): `location.center.scenes.StreetChallenge1.executedToday`, `location.house.scenes.PizzaDelivery.executedToday`, `location.bus.scenes.BusFlash.executedToday`, `location.bus.scenes.BusMasturbate.executedToday`, `location.bus.scenes.BusGrope.executedToday`, `location.photoStudio.scenes.ModelPhotoshoot.executedToday`, …
- **gallery** (142): `location.center.scenes.StreetChallenge1.gallery`, `location.house.scenes.PizzaDelivery.gallery`, `location.bus.scenes.BusFlash.gallery`, `location.bus.scenes.BusMasturbate.gallery`, `location.bus.scenes.BusGrope.gallery`, `location.photoStudio.scenes.ModelPhotoshoot.gallery`, …
- **inside** (142): `location.center.scenes.StreetChallenge1.inside`, `location.house.scenes.PizzaDelivery.inside`, `location.bus.scenes.BusFlash.inside`, `location.bus.scenes.BusMasturbate.inside`, `location.bus.scenes.BusGrope.inside`, `location.photoStudio.scenes.ModelPhotoshoot.inside`, …
- **blowjob** (142): `location.center.scenes.StreetChallenge1.blowjob`, `location.house.scenes.PizzaDelivery.blowjob`, `location.bus.scenes.BusFlash.blowjob`, `location.bus.scenes.BusMasturbate.blowjob`, `location.bus.scenes.BusGrope.blowjob`, `location.photoStudio.scenes.ModelPhotoshoot.blowjob`, …
- **threesome** (142): `location.center.scenes.StreetChallenge1.threesome`, `location.house.scenes.PizzaDelivery.threesome`, `location.bus.scenes.BusFlash.threesome`, `location.bus.scenes.BusMasturbate.threesome`, `location.bus.scenes.BusGrope.threesome`, `location.photoStudio.scenes.ModelPhotoshoot.threesome`, …
- **gangbang** (142): `location.center.scenes.StreetChallenge1.gangbang`, `location.house.scenes.PizzaDelivery.gangbang`, `location.bus.scenes.BusFlash.gangbang`, `location.bus.scenes.BusMasturbate.gangbang`, `location.bus.scenes.BusGrope.gangbang`, `location.photoStudio.scenes.ModelPhotoshoot.gangbang`, …
- **corruption** (97): `player.clothing.corruption`, `player.lastClothing.corruption`, `player.scenes.XCam.requirementsMC.corruption`, `player.scenes.BathroomLactation.requirementsMC.corruption`, `player.scenes.XCamBlackmail.requirementsMC.corruption`, `player.scenes.HouseCleaning1.requirementsMC.corruption`, …
- **location** (63): `location.school.MathClass.location`, `location.school.HistoryClass.location`, `location.school.ComputerClass.location`, `location.school.PEClass.location`, `location.school.EmptyClass.location`, `location.mall.subLocations.techStore.location`, …
- **arousal** (55): `player.arousal`, `player.drugs.modifiers.arousal`, `npc.Dad.arousal`, `npc.Brother.arousal`, `npc.Grandpa.arousal`, `npc.Marcus.arousal`, …
- **avatar** (54): `player.avatar`, `npc.Dad.avatar`, `npc.Brother.avatar`, `npc.Grandpa.avatar`, `npc.Marcus.avatar`, `npc.Sam.avatar`, …
- **key** (53): `npc.Dad.key`, `npc.Brother.key`, `npc.Grandpa.key`, `npc.Marcus.key`, `npc.Sam.key`, `npc.Oliver.key`, …
- **gender** (53): `npc.Dad.gender`, `npc.Brother.gender`, `npc.Grandpa.gender`, `npc.Marcus.gender`, `npc.Sam.gender`, `npc.Oliver.gender`, …

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-19T07:03:50.326Z | 15m 12s | 32 | 32 | 40 | no |
| 2 | 2026-04-19T07:28:14.909Z | 29m 32s | 33 | 33 | 76 | no |
| 3 | 2026-04-19T09:35:38.205Z | 16m 1s | 13 | 13 | 51 | no |
| 4 | 2026-04-19T10:06:22.727Z | 10m 7s | 12 | 12 | 67 | no |
| 5 | 2026-04-19T10:20:53.668Z | 11m 45s | 13 | 13 | 38 | no |
| 6 | 2026-04-19T10:37:42.108Z | 6m 31s | 3 | 3 | 54 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **496**
- Observed edges during play: **102** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **30** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **78**.
- Coverage: **6.05%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 264

### Playable-content partition
- Passages defined in source: **358** (0 tagged `wip`, 1 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **357**.
- Distinct passages visited at least once: **50** — playable-passage coverage: **14.0%**.

### Static edge kinds
| kind | count |
|---|---|
| button | 375 |
| goto | 76 |
| include | 45 |

## See also
- `variable_profile.json` — raw statistical evidence, no labels
- `variable_schema.json` — variables with applied labels + confidence
- `mechanics.md` — design patterns observed
- `coverage.md` — frontier + explored counts
- `static_graph.json` — every navigation edge parsed from passage source (M2, written at startup as of M6.1)
- `choice_graph.json` — observed edges with per-edge effect aggregates (M2)
- `variable_index.json` — every game variable → passages/edges that `<<set>>`/`<<unset>>` it, with enclosing `<<if>>` gates (M6.1)
- `passage_catalog.json` — every passage with raw source + tags (M1)
- `scene_bodies.jsonl` — full rendered body per unique state (M1)
- `initial_state.json` — pristine pre-Phase-0a snapshot (M1)
- `state_timeline.jsonl` — per-observation state + full diff values (M1)
- `engine_config.json` — SugarCube Config/Setting/version/save-caps + State.history shape + Story IFID (M3)
- `sidebar_snapshots.jsonl` — sidebar panel text captures across Phase 0 probes + passive mid-game changes (M4)