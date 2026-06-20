# dol_creator — Exploration Report

Generated: 2026-06-18T12:53:22.635Z
Source URL: https://mopoga.com/degrees-of-lewdity

## Session Summary

- Sessions run: 1
- Total wall-clock: 8m 33s
- Total clicks: 5
- Total choices explored: 5
- Unique states seen: 10
- Unexplored frontier (queued for next session): 0
- Endings reached: 1 (Mirror)

## Engine
Detected engine: **sugarcube** v(revive:eval),(short(){const prerelease=this.prerelease?`-${this.prerelease}`:"";return`${this.title} (v${this.major}.${this.minor}.${this.patch}${prerelease})`})

## Variable schema (labeled at report time)

### player_stat (9)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `money` | number | 500..500 | 0 | high |
| `willpower` | number | 200..200 | 0 | high |
| `beauty` | number | 100..1428.5714285714287 | 1 | high |
| `hunger` | number | 0..0 | 0 | high |
| `drunk` | number | 0..0 | 0 | high |
| `featsBoosts.upgrades.money` | number | 0..0 | 0 | high |
| `featsBoosts.missing.money` | string | `Unlock this boost by` | 0 | high |
| `featsBoosts.name.money` | string | `?????` | 0 | high |
| `docks.slave.money` | number | 0..0 | 0 | high |

### npc_stat (8)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `earSlime.corruption` | number | 0..0 | 0 | high |
| `nectar_addiction` | number | 0..0 | 0 | high |
| `enemytrust` | number | 0..0 | 0 | high |
| `audiencearousal` | number | 0..0 | 0 | high |
| `wolfpacktrust` | number | 0..0 | 0 | high |
| `wolfpackfear` | number | 0..0 | 0 | high |
| `trackedArousal` | object | — | 0 | high |
| `timeSinceArousal` | number | 0..0 | 0 | high |

### body (105)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `settings.breastModifier` | number | 0..0 | 0 | medium |
| `settings.darkSkinChance` | number | 10..10 | 0 | medium |
| `settings.bodyWritingLevel` | number | 3..3 | 0 | medium |
| `settings.clothingCostModifier` | number | 1..1 | 0 | medium |
| `settings.schoolClothingCostModifier` | number | 1..1 | 0 | medium |
| `settings.lewdClothingCostModifier` | number | 1..1 | 0 | medium |
| `settings.basePlayerPregnancyChance` | number | 80..80 | 0 | medium |
| `settings.baseNpcPregnancyChance` | number | 8..8 | 0 | medium |
| `settings.humanPregnancyMonths` | number | 3..3 | 0 | medium |
| `settings.wolfPregnancyWeeks` | number | 4..4 | 0 | medium |
| `settings.pregnancyType` | string | `realistic` | 0 | medium |
| `objectVersion.skinColor` | number | 1..1 | 0 | medium |
| `objectVersion.npcPregnancyGenderChange` | number | 1..1 | 0 | medium |
| `objectVersion.pregnancyAvoidance` | number | 1..1 | 0 | medium |
| `clothing_update` | number | 1..1 | 0 | medium |
| `player.breastsize` | number | 0..4 | 1 | medium |
| `player.gender_body` | string | `a` | 0 | medium |
| `player.bodyTemperature` | number | 37..37 | 0 | medium |
| `player.bodyshape` | string | `classic`, `curvy` | 1 | medium |
| `carried.over_upper.bustresize` | number | 0..0 | 0 | medium |
| `carried.over_upper.breast_img` | number | 0..0 | 0 | medium |
| `carried.upper.bustresize` | number | 0..0 | 0 | medium |
| `carried.upper.breast_img` | number | 0..0 | 0 | medium |
| `carried.under_upper.bustresize` | number | 0..0 | 0 | medium |
| `carried.under_upper.breast_img` | number | 0..0 | 0 | medium |
| `worn.over_upper.bustresize` | number | 0..0 | 0 | medium |
| `worn.over_upper.breast_img` | number | 0..0 | 0 | medium |
| `worn.upper.bustresize` | number | 0..0 | 0 | medium |
| `worn.upper.breast_img` | number | 0..0 | 0 | medium |
| `worn.under_upper.bustresize` | number | 0..0 | 0 | medium |
| `worn.under_upper.breast_img` | number | 0..0 | 0 | medium |
| `outfit` | object | — | 0 | medium |
| `wear_outfit` | string | `none` | 0 | medium |
| `parasite.bodyparts` | object | — | 0 | medium |
| `hairlength` | number | 200..200 | 0 | medium |
| `hairtype` | string | `default` | 0 | medium |
| `breastsizeold` | number | 0..0 | 0 | medium |
| `breastsizemax` | number | 12..12 | 0 | medium |
| `breastsizemin` | number | 0..0 | 0 | medium |
| `breastsensitivity` | number | 1..1 | 0 | medium |
| … | … | … | … | and 65 more |

### item (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `internet.photos` | object | — | 0 | medium |

### flag (266)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `settings.maleChanceSplit` | boolean | false | 0 | high |
| `settings.beastMaleChanceSplit` | boolean | false | 0 | high |
| `settings.monsterHallucinationsOnly` | boolean | true | 0 | high |
| `settings.swarmsEnabled` | boolean | true | 0 | high |
| `settings.spidersEnabled` | boolean | true | 0 | high |
| `settings.slugsEnabled` | boolean | true | 0 | high |
| `settings.waspsEnabled` | boolean | true | 0 | high |
| `settings.beesEnabled` | boolean | true | 0 | high |
| `settings.lurkersEnabled` | boolean | true | 0 | high |
| `settings.horsesEnabled` | boolean | true | 0 | high |
| `settings.parasitesEnabled` | boolean | true | 0 | high |
| `settings.ruinedOrgasmEnabled` | boolean | true | 0 | high |
| `settings.bestialityEnabled` | boolean | true | 0 | high |
| `settings.slimesEnabled` | boolean | true | 0 | high |
| `settings.voreEnabled` | boolean | true | 0 | high |
| `settings.tentaclesEnabled` | boolean | true | 0 | high |
| `settings.plantsEnabled` | boolean | true | 0 | high |
| `settings.analEnabled` | boolean | true | 0 | high |
| `settings.analDoubleEnabled` | boolean | true | 0 | high |
| `settings.analingusGivingEnabled` | boolean | true | 0 | high |
| `settings.analingusReceivingEnabled` | boolean | true | 0 | high |
| `settings.vaginalDoubleEnabled` | boolean | true | 0 | high |
| `settings.transformAnimalEnabled` | boolean | true | 0 | high |
| `settings.transformDivineEnabled` | boolean | true | 0 | high |
| `settings.pubicHairEnabled` | boolean | false | 0 | high |
| `settings.breastFeedingEnabled` | boolean | true | 0 | high |
| `settings.parasitePregnancyEnabled` | boolean | true | 0 | high |
| `settings.footFetishEnabled` | boolean | true | 0 | high |
| `settings.toyWhipEnabled` | boolean | true | 0 | high |
| `settings.toyDildoEnabled` | boolean | true | 0 | high |
| `settings.toyMultiplePenetrationEnabled` | boolean | true | 0 | high |
| `settings.pregnancySpeechEnabled` | boolean | true | 0 | high |
| `settings.hypnosisEnabled` | boolean | true | 0 | high |
| `settings.blindStatsEnabled` | boolean | false | 0 | high |
| `settings.watersportsEnabled` | boolean | false | 0 | high |
| `settings.facesitEnabled` | boolean | true | 0 | high |
| `settings.forcedCrossdressingEnabled` | boolean | true | 0 | high |
| `settings.playerPregnancyHumanEnabled` | boolean | true | 0 | high |
| `settings.playerPregnancyBeastEnabled` | boolean | true | 0 | high |
| `settings.playerPregnancyEggLayingEnabled` | boolean | true | 0 | high |
| … | … | … | … | and 226 more |

### scalar (1961)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `startDate` | number | 63797871600..63797871600 | 0 | low |
| `timeStamp` | number | -2099700..0 | 1 | low |
| `weatherObj.snow` | number | 0..0 | 0 | low |
| `weatherObj.previousWeatherIndex` | number | 0..4 | 1 | low |
| `settings.maleChance` | number | 50..50 | 0 | low |
| `settings.maleChanceMale` | number | 50..50 | 0 | low |
| `settings.maleChanceFemale` | number | 50..50 | 0 | low |
| `settings.maleVictimChance` | number | 50..50 | 0 | low |
| `settings.beastMaleChance` | number | 75..80 | 1 | low |
| `settings.beastMaleChanceMale` | number | 80..80 | 0 | low |
| `settings.beastMaleChanceFemale` | number | 80..80 | 0 | low |
| `settings.monsterChance` | number | 20..50 | 1 | low |
| `settings.allureModifier` | number | 1..1 | 0 | low |
| `settings.tendingYieldModifier` | number | 5..5 | 0 | low |
| `settings.femaleNPCPenisChance` | number | 0..0 | 0 | low |
| `settings.maleNPCVaginaChance` | number | 0..0 | 0 | low |
| `settings.straponChance` | number | 0..0 | 0 | low |
| `settings.penisModifier` | number | 0..0 | 0 | low |
| `settings.asphyxiaLevel` | number | 3..3 | 0 | low |
| `settings.nudeGenderPerception` | number | 1..1 | 0 | low |
| `settings.npcVirginChanceStudent` | number | 50..50 | 0 | low |
| `settings.npcVirginChanceAdult` | number | 10..10 | 0 | low |
| `settings.underwearCostModifier` | number | 1..1 | 0 | low |
| `settings.furnitureCostModifier` | number | 1..1 | 0 | low |
| `settings.rentCostModifier` | number | 1..1 | 0 | low |
| `settings.condomLevel` | number | 3..3 | 0 | low |
| `settings.condomChance` | number | 60..60 | 0 | low |
| `settings.condomUseChanceRape` | number | 33..33 | 0 | low |
| `settings.condomUseChanceConsensual` | number | 83..83 | 0 | low |
| `options.images` | number | 1..1 | 0 | low |
| `options.combatImages` | number | 1..1 | 0 | low |
| `options.lightSpotlight` | number | 0.2..0.2 | 0 | low |
| `options.lightGradient` | number | 0.1..0.1 | 0 | low |
| `options.lightGlow` | number | 0.1..0.1 | 0 | low |
| `options.lightFlat` | number | 0..0 | 0 | low |
| `options.lightTFColor` | number | 0.2..0.2 | 0 | low |
| `options.combatLightSpotlight` | number | 0.2..0.2 | 0 | low |
| `options.combatLightSpotlightX` | number | 118..118 | 0 | low |
| `options.combatLightSpotlightY` | number | 15..15 | 0 | low |
| `options.combatLightOffsetY` | number | 52..52 | 0 | low |
| … | … | … | … | and 1921 more |

### string (545)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `weatherObj.starSeed` | string | `NzE0Mg==`, `MjY2Ng==` | 1 | low |
| `passagePrev` | string | `none`, `Start`, `Start2` | 4 | low |
| `passage` | string | `Start`, `Start2`, `Orphanage Intro` | 4 | low |
| `settings.skillCheckStyle` | string | `words` | 0 | low |
| `settings.multipleWardrobes` | string | `isolated` | 0 | low |
| `options.sidebarStats` | string | `all` | 0 | low |
| `options.sidebarTime` | string | `top` | 0 | low |
| `options.combatControls` | string | `radio` | 0 | low |
| `options.pepperSprayDisplay` | string | `sprays` | 0 | low |
| `options.condomsDisplay` | string | `standard` | 0 | low |
| `options.timestyle` | string | `military` | 0 | low |
| `options.tipdisable` | string | `f` | 0 | low |
| `options.passageCount` | string | `disabled` | 0 | low |
| `options.traitOverlayFormat` | string | `table` | 0 | low |
| `options.debugdisable` | string | `t` | 0 | low |
| `options.dateFormat` | string | `en-GB` | 0 | low |
| `lastWardrobeSlot` | string | `head` | 0 | low |
| `gamemode` | string | `normal` | 0 | low |
| `player.gender` | string | `f`, `n` | 1 | low |
| `player.sex` | string | `f`, `h` | 1 | low |
| `player.skin.color` | string | `light` | 0 | low |
| `carried.over_upper.slot` | string | `over_upper` | 0 | low |
| `carried.over_upper.name` | string | `naked` | 0 | low |
| `carried.over_upper.name_cap` | string | `Naked` | 0 | low |
| `carried.over_upper.variable` | string | `naked` | 0 | low |
| `carried.over_upper.word` | string | `n` | 0 | low |
| `carried.over_upper.gender` | string | `n` | 0 | low |
| `carried.over_upper.description` | string | `naked` | 0 | low |
| `carried.over_upper.lastTaken` | string | `wardrobe` | 0 | low |
| `carried.over_lower.slot` | string | `over_lower` | 0 | low |
| `carried.over_lower.name` | string | `naked` | 0 | low |
| `carried.over_lower.name_cap` | string | `Naked` | 0 | low |
| `carried.over_lower.variable` | string | `naked` | 0 | low |
| `carried.over_lower.word` | string | `n` | 0 | low |
| `carried.over_lower.gender` | string | `n` | 0 | low |
| `carried.over_lower.description` | string | `naked` | 0 | low |
| `carried.over_lower.lastTaken` | string | `wardrobe` | 0 | low |
| `carried.upper.slot` | string | `upper` | 0 | low |
| `carried.upper.name` | string | `naked` | 0 | low |
| `carried.upper.name_cap` | string | `Naked` | 0 | low |
| … | … | … | … | and 505 more |

### misc (547)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `weatherObj.monthlyTemperatures` | object | — | 0 | low |
| `weatherObj.keypointsArr` | object | — | 0 | low |
| `weatherObj.fogKeypoints` | object | — | 0 | low |
| `tags` | object | — | 0 | low |
| `saveVersions` | object | — | 0 | low |
| `player.skin.layers` | object | — | 0 | low |
| `NPCList` | object | — | 0 | low |
| `BeastList` | object | — | 0 | low |
| `NPCName` | object | — | 0 | low |
| `NPCNameList` | object | — | 0 | low |
| `store.over_upper` | object | — | 0 | low |
| `store.over_lower` | object | — | 0 | low |
| `store.upper` | object | — | 0 | low |
| `store.lower` | object | — | 0 | low |
| `store.under_upper` | object | — | 0 | low |
| `store.under_lower` | object | — | 0 | low |
| `store.over_head` | object | — | 0 | low |
| `store.head` | object | — | 0 | low |
| `store.face` | object | — | 0 | low |
| `store.neck` | object | — | 0 | low |
| `store.hands` | object | — | 0 | low |
| `store.handheld` | object | — | 0 | low |
| `store.legs` | object | — | 0 | low |
| `store.feet` | object | — | 0 | low |
| `store.genitals` | object | — | 0 | low |
| `wardrobe.over_upper` | object | — | 0 | low |
| `wardrobe.over_lower` | object | — | 0 | low |
| `wardrobe.upper` | object | — | 0 | low |
| `wardrobe.lower` | object | — | 0 | low |
| `wardrobe.under_upper` | object | — | 0 | low |
| `wardrobe.under_lower` | object | — | 0 | low |
| `wardrobe.over_head` | object | — | 0 | low |
| `wardrobe.head` | object | — | 0 | low |
| `wardrobe.face` | object | — | 0 | low |
| `wardrobe.neck` | object | — | 0 | low |
| `wardrobe.hands` | object | — | 0 | low |
| `wardrobe.handheld` | object | — | 0 | low |
| `wardrobe.legs` | object | — | 0 | low |
| `wardrobe.feet` | object | — | 0 | low |
| `wardrobe.genitals` | object | — | 0 | low |
| … | … | … | … | and 507 more |

## NPCs detected

| npc | stats observed | var count |
|---|---|---|
| earslime | corruption | 1 |
| nectar | addiction | 1 |
| enemy | trust | 1 |
| audience | arousal | 1 |
| wolfpack | trust, fear | 2 |
| tracked | arousal | 1 |
| timesince | arousal | 1 |

## Body / appearance traits

- `settings.breastModifier`
- `settings.darkSkinChance`
- `settings.bodyWritingLevel`
- `settings.clothingCostModifier`
- `settings.schoolClothingCostModifier`
- `settings.lewdClothingCostModifier`
- `settings.basePlayerPregnancyChance`
- `settings.baseNpcPregnancyChance`
- `settings.humanPregnancyMonths`
- `settings.wolfPregnancyWeeks`
- `settings.pregnancyType`
- `objectVersion.skinColor`
- `objectVersion.npcPregnancyGenderChange`
- `objectVersion.pregnancyAvoidance`
- `clothing_update`
- `player.breastsize`
- `player.gender_body`
- `player.bodyTemperature`
- `player.bodyshape`
- `carried.over_upper.bustresize`
- `carried.over_upper.breast_img`
- `carried.upper.bustresize`
- `carried.upper.breast_img`
- `carried.under_upper.bustresize`
- `carried.under_upper.breast_img`
- `worn.over_upper.bustresize`
- `worn.over_upper.breast_img`
- `worn.upper.bustresize`
- `worn.upper.breast_img`
- `worn.under_upper.bustresize`

Transitions observed: 2
- `player.breastsize`: `0` → `4` at `Start`
- `player.bodyshape`: `"classic"` → `"curvy"` at `Start`

## Choice type distribution

_No choices classified yet._

## Economy

- Price-labeled choices observed: 0
- Money income events: 0
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **amount** (152): `foodstuff.apple.amount`, `foodstuff.apple_crumble.amount`, `foodstuff.apple_strudel.amount`, `foodstuff.arancini.amount`, `foodstuff.baby_bottle_of_breast_milk.amount`, `foodstuff.bacon.amount`, …
- **accessory** (91): `carried.over_upper.accessory`, `carried.over_upper.accessory_colour`, `carried.over_upper.accessory_colour_options`, `carried.over_lower.accessory`, `carried.over_lower.accessory_colour`, `carried.over_lower.accessory_colour_options`, …
- **name** (82): `carried.over_upper.name`, `carried.over_upper.name_cap`, `carried.over_lower.name`, `carried.over_lower.name_cap`, `carried.upper.name`, `carried.upper.name_cap`, …
- **state** (73): `carried.over_upper.state`, `carried.over_upper.state_base`, `carried.over_upper.state_top`, `carried.over_upper.state_top_base`, `carried.over_lower.state`, `carried.over_lower.state_base`, …
- **colour** (69): `carried.over_upper.colour`, `carried.over_upper.colour_options`, `carried.over_lower.colour`, `carried.over_lower.colour_options`, `carried.upper.colour`, `carried.upper.colour_options`, …
- **integrity** (60): `carried.over_upper.integrity`, `carried.over_upper.integrity_max`, `carried.over_lower.integrity`, `carried.over_lower.integrity_max`, `carried.upper.integrity`, `carried.upper.integrity_max`, …
- **over** (51): `store.over_upper`, `store.over_lower`, `store.over_head`, `wardrobe.over_upper`, `wardrobe.over_lower`, `wardrobe.over_head`, …
- **cost** (48): `carried.over_upper.cost`, `carried.over_lower.cost`, `carried.upper.cost`, `carried.lower.cost`, `carried.under_upper.cost`, `carried.under_lower.cost`, …
- **gender** (37): `player.gender`, `player.gender_body`, `carried.over_upper.gender`, `carried.over_lower.gender`, `carried.upper.gender`, `carried.lower.gender`, …
- **type** (34): `carried.over_upper.type`, `carried.over_lower.type`, `carried.upper.type`, `carried.lower.type`, `carried.under_upper.type`, `carried.under_lower.type`, …
- **under** (32): `store.under_upper`, `store.under_lower`, `wardrobe.under_upper`, `wardrobe.under_lower`, `wardrobes.changingRoom.under_lower`, `wardrobes.changingRoom.under_upper`, …
- **index** (31): `carried.over_upper.index`, `carried.over_lower.index`, `carried.upper.index`, `carried.lower.index`, `carried.under_upper.index`, `carried.under_lower.index`, …
- **description** (31): `carried.over_upper.description`, `carried.over_lower.description`, `carried.upper.description`, `carried.lower.description`, `carried.under_upper.description`, `carried.under_lower.description`, …
- **location** (31): `carried.over_upper.location`, `carried.over_lower.location`, `carried.upper.location`, `carried.lower.location`, `carried.under_upper.location`, `carried.under_lower.location`, …
- **slot** (30): `carried.over_upper.slot`, `carried.over_lower.slot`, `carried.upper.slot`, `carried.lower.slot`, `carried.under_upper.slot`, `carried.under_lower.slot`, …
- **variable** (30): `carried.over_upper.variable`, `carried.over_lower.variable`, `carried.upper.variable`, `carried.lower.variable`, `carried.under_upper.variable`, `carried.under_lower.variable`, …
- **fabric** (30): `carried.over_upper.fabric_strength`, `carried.over_lower.fabric_strength`, `carried.upper.fabric_strength`, `carried.lower.fabric_strength`, `carried.under_upper.fabric_strength`, `carried.under_lower.fabric_strength`, …
- **reveal** (30): `carried.over_upper.reveal`, `carried.over_lower.reveal`, `carried.upper.reveal`, `carried.lower.reveal`, `carried.under_upper.reveal`, `carried.under_lower.reveal`, …
- **word** (30): `carried.over_upper.word`, `carried.over_lower.word`, `carried.upper.word`, `carried.lower.word`, `carried.under_upper.word`, `carried.under_lower.word`, …
- **plural** (30): `carried.over_upper.plural`, `carried.over_lower.plural`, `carried.upper.plural`, `carried.lower.plural`, `carried.under_upper.plural`, `carried.under_lower.plural`, …

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-06-18T12:44:49.142Z | 8m 33s | 5 | 5 | 10 | yes |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **35619**
- Observed edges during play: **1** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **0** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **1**.
- Coverage: **0.00%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 7

### Playable-content partition
- Passages defined in source: **15431** (0 tagged `wip`, 0 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **15431**.
- Distinct passages visited at least once: **5** — playable-passage coverage: **0.0%**.

### Static edge kinds
| kind | count |
|---|---|
| link | 35532 |
| include | 73 |
| wiki | 14 |

### Unresolved static targets (67)
Targets that appear in passage source but don't resolve to a known passage — typically dynamic expressions like `` <<goto `func()`>> `` or referenced-but-never-defined passages.

- `"School Boy's Toilets"`
- `"School Girl's Toilets"`
- `"https://degreesoflewdity.miraheze.org/wiki/Main_Page"`
- `"https://discord.gg/VznUtEh"`
- `"https://gitgud.io/Vrelnir/degrees-of-lewdity"`
- `"https://subscribestar.adult/vrelnir"`
- `"https://vrelnir.blogspot.com"`
- `"https://vrelnir.fanbox.cc/"`
- `"https://www.vrelnir.com"`
- `Elk Compound Lab Enter`
- `Estate Manor Approach Defeat`
- `Estate Manor Intro Entrance`
- `Flats Window`
- `Forest Trunks Caught`
- `Forest Trunks Cower`
- `Forest Trunks Howl`
- `Forest Trunks Run`
- `Gwylan Talk Clothes Succubus Refuse`
- `Livestock Barn Night`
- `Mansion Intro 9 Push`
- … and 47 more

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