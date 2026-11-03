# [READY] Scene — zoe_dares

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118). Zoe's hot repeatable, from her signed release-1 ladder
> (`sheets/people/npc_zoe.md`, "The dares"). Replaces the built `party_dare` (`iterations/002/build_scripts/pools.py:87`;
> its sheet is marked reworked). Six dare screens written by `v2-prose` and measured, plus the built circle flash kept;
> the other lines are mine.

| row | answer |
|---|---|
| system · place | parties · Zoe's apartment (Friday) and the party house (Saturday), her party hours |
| gate | `picks_the_dares` (Zoe's step 4) · Zoe present · a party tonight · not dared tonight (`zoe_dared_today`, cleared by the daily tick) · each yes by its stage (DECISIONS 124): the kiss Curious, every dare the room watches Exhibitionism 60, cap 79 |
| BRAKE | **one dare a night** (was two) |
| who picks | Zoe. Her line names the dare; the screen offers a showing yes, a doing yes and the no (`meters.md` rule 5) |
| which tier | after Zoe's step 5 (`zoe_together`): **Zoe joins** · else Corruption 40 or Exhibitionism 40: **Bold · Showing** · else **Curious · Daring**. Each yes shows by its own meter (below); a yes she can't take shows locked with the number |
| Corruption 60 | a fourth button, locked: "Zoe's next dare. (Needs Corruption 60.)" |
| who sees | the room, every time |
| counts | each yes: `zoe_dares_done` add +1 (Zoe's step 5 needs 4) |
| the crude-word ceiling | Zoe's early and middle columns (tits, ass, nipples, wet), with thighs; his cock only through his jeans on the two lap dares (plain anatomy beside her column, as Ryan's and Hale's signed sheets) · no pussy, clit, fuck, cunt, cum. confirmed by LO 2026-11-01 ("Continue") the cock |
| truth | repeats: no "first time", no "again", no history |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." | Both lines sit inside the beats. |

## The dares by tier

| tier | Zoe's line | showing yes | doing yes | the no |
|---|---|---|---|---|
| Curious · Daring | "Flash the guy at the keg. Or kiss the cocky guy. Properly. Pick." | "Watch me." (Exhibitionism 20) → `low_show` · exhibitionism add +1 | "Watch this." (Corruption 20) → `low_do` · corruption add +1 · exhibitionism add +1 (seen) | "Not tonight." |
| Bold · Showing | "Topless in the kitchen till the song ends. Or his lap, till he's hard. Make him beg." | "Start the song." (Exhibitionism 40) → `high_show` (a two-entry pool with the built circle flash) · exhibitionism add +1 · corruption add +1 | "Easy." (Corruption 40 and Exhibitionism 20, mixed) → `high_do` · corruption add +1 · exhibitionism add +1 | "Not tonight." |
| Zoe joins (after step 5) | "Kiss me where they can see. Or let me watch you with him." | "Here?" → `z_show` · both add +1 | "Watch, then." → `z_do` · both add +1 | "Not tonight." |

Every pay is under her stage cap (19 / 39 / 59, DECISIONS 78). **The no:** Zoe pouts, "Boo. Next one's tamer." No cost
but the meter.

## The regulars remember
- A dare with the guy at the keg sets `keg_guy_dared`; with the cocky guy, `cocky_guy_dared`. At the next party, his
  line: keg guy, "You again. I'm keeping my cup this time." · cocky guy, "You again. Where's my beer?" Mine.
- **Jake** (`jake_step` gte 3, her boyfriend): a dare with a man adds one line. Cocky guy: "He's Jake's teammate. He'll
  tell Jake, or he won't." (`extras.py:68`: "Jake's teammate") · keg guy: "Half this party knows Jake." Jake finding out is
  a later release.

## The dares, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Where the tool lists `cock` on a beat with "the cocky guy", it is matching "cocky" (a false reading, like its `vaginal` rung); the counts below leave it out.

### Curious · Daring

**`low_show`** · 136 words · explicit words 5 · median sentence 9

> You walk straight to the keg with Zoe laughing behind you. The guy in the backwards cap is pumping it. You stand right in front of him and wait. He looks up. You grab your top and yank it up to your chin. Your tits are bare to him in the middle of the party. He freezes with the pump in his fist. Beer foams over his cup. Someone by the keg cheers. *Let the whole room look.* Your heart is slamming, and you hold it there one long second. The air is cold on your bare tits. Your nipples go tight and hard while he stares at them. Your face burns. You're wet, and your thighs press together. You pull your top down over your hard nipples, and your tits still tingle under it.

**`low_do`** · 128 words · explicit words 6 · median sentence 11 · act rungs: touch · also played by Zoe's step 2, "Dare me something else."

> You take the beer out of his hand and set it on the counter. He opens his mouth to say something, and you kiss it shut. Properly. Your tongue slides over his, slow, and his pushes back. Someone whoops, then the whole corner does. His hands drop to your ass and squeeze hard, one cheek filling each palm. He pulls you in until your tits press flat against his chest. Your nipples go hard under your top, and he feels them. It's a dare. It doesn't count. Over his shoulder Zoe is biting her lip, eyes on your mouth. You kiss him deeper anyway, wet and open. Then you pull back first, breathing hard, lips wet. He grins down at you, both hands still full of your ass.

### Bold · Showing

**`high_show`** · 129 words · explicit words 4 · median sentence 9

> "Start the song," you say, and Zoe hits play. You pull your top off over your head and drop it on the counter. Your tits are bare under the kitchen light. The guys by the fridge stop talking. The guy at the keg stops pumping and stares from the doorway, cap backwards, mouth open. You pour a drink and lean on the counter, ass pushed back. Someone lifts a phone and Zoe slaps it down. "Eyes only," she yells. Your nipples are hard and tight in the open air. You're wet, and you don't cover up. "Look all you want," you tell the room. You want her to dare you something worse. The song hits its last beat, and every eye in the kitchen is on your bare tits.

**`high_show`, entry two:** the built circle flash (`pools.py:85`, signed in `party_dare.md`), Zoe's line "Flash them, babe. Three seconds."

**`high_do`** · 137 words · explicit words 9 · median sentence 9 · act rungs: hands · a mixed act, seen

> The cocky guy grins up at you from the couch, beer still in his hand. You sit in his lap facing the room. Then you grind your ass down on him, slow. His cock gets hard under you, thick through his jeans. His hands grab your hips and hold on. He groans into your neck. One hand slides up toward your tits, but you push it back down. "Not those," you tell him. "Say please." You roll your ass over his cock until his breath shakes. "Please," he says, loud. The people on the couch hear it and laugh. Zoe watches from the arm of the couch, grinning. "Good boy," she says. Your nipples are tight against your top, and you're wet. You keep grinding. He begs into your neck, and his cock jerks under your ass.

### Zoe joins (after step 5)

**`z_show`** · 116 words · explicit words 7 (8 listed, one is "cocky") · median sentence 6 · act rungs: touch

> You grab her face and kiss her, right there in the middle of the room. Her mouth opens under yours. Her tongue finds yours, slow and greedy. Her hands go into your hair, then slide down to your ass to pull you in hard. Your tits press flat against hers. Her thigh pushes between yours. You grind down on it. The room goes loud, whistles and shouting over the music. Then it goes quiet. Everyone stares. The cocky guy stands by the wall, his beer stopped halfway to his mouth. Zoe grins into the kiss. She squeezes your ass harder and drags you tighter onto her thigh. You're wet. Your nipples are hard against her tits.

**`z_do`** · 120 words · explicit words 7 (8 listed, one is "cocky") · median sentence 12 · act rungs: touch, hands

> The cocky guy on the corner couch grins up at you and sets his beer on the floor. You straddle his lap and kiss him hard, with the whole room watching. His hands slide up under your top and close on your bare tits. His cock is hard under you through his jeans, and your hips roll on it. Zoe sits right beside you, close enough to touch. Her hand rests on your thigh. "Slower," she tells him, and he slows. His thumbs find your nipples. "Her nipples. Yes. Like that." You keep your eyes on Zoe while he touches you. You're wet, grinding down on his cock. His hands squeeze your tits, and Zoe's fingers press into your thigh.

Every last sentence is on the body. None has her come; the dares stop where the release's door is.

## What the built `party_dare` loses
- "Dare Zoe instead." and its kiss screen (Ella picking): Zoe picks now.
- Two dares a night: one now.
- Its gate (Exhibitionism 40, Friday after 23:00): the dares open at step 4, both party nights.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the dares by stage, the two yeses, the pays, the no, the regulars, Jake's line, the locked line | `proposals/ZOE_R1_LADDER.md`, "The dares" (signed 2026-11-01) |
| one a night, Zoe picks | the same |
| the circle flash kept | `party_dare.md` (signed 2026-10-09) |
| the "You again." lines, the counter, the flags | mine, confirmed by LO 2026-11-01 ("Continue") |

### False lines a3, 2026-11-02 (DECISIONS 129)
Zoe's dare says "till the song ends", but the pool's second entry (the circle flash) counted to three. `high_show`
entry two is now `FLASH_SONG` (`pools.py`): "Till the song ends, babe," and she holds them out past the last note.
108 words, 4 explicit (the circle flash it replaces: 97, 4). The circle flash itself stays in `party_dare`.

