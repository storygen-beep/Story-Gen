# [READY] Scene — zoe_02_bra_through_the_sleeve

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): seen by the readers, the `sleeve` button "Give it back." became "Ask for it back." (Zoe doesn't have the bra yet when it shows; the build).

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118): Zoe's release-1 ladder (`sheets/people/npc_zoe.md`, signed). Changed: the gate is Curious **or** Daring (`meters.md` rule 5: a showing yes and a doing yes on one screen); a doing yes added, "Dare me something else.", which plays the dares' kiss screen; her voice row.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 2 (Zoe A 2) |
| where · when | Zoe's balcony, a Friday party · 21:00–00:00 |
| gate | her step 1 · 24 hours after step 1 · the boost off · "Watch me." Exhibitionism 20 · "Dare me something else." Corruption 20 with the cocky guy there |
| want | she keeps her eyes on the bra strap |
| next step | a dress dare with the room behind the glass |
| hook | "Nope. Mine now." And: "There's a hot tub Saturday. Just us." |
| what she wears here | the dress in a group on `zoe_party_dress` worn; the bra comes off here |
| explicit? | the showing path no (under 3 list words, as built); the doing path yes (the kiss, `zoe_dares` `low_do`) |
| who notices | the room behind the glass |
| what she risks | strangers seeing |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." (the person sheet's pair) | |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** a dare for one person she knows, the party behind the glass · Daring (Exhibitionism 20), or a kiss at Curious

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| on the balcony she unhooks her bra and pulls it out through her sleeve | Zoe; the party through the glass door | strangers seeing | "Watch me." · or "Dare me something else." (kiss the cocky guy) | the dare; she keeps the bra: "Mine now." | yes | her step 2; `party_house_invite`: "There's a hot tub Saturday." |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_02_bra_through_the_sleeve`** — Zoe's Living Room · Fri 21:00-00:00 · Zoe there · needs Zoe's step = 1 · drinks boost off · 24h+ since `zoe_01_done` · Exhibitionism 20+ · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `balcony` | Zoe pulls you out onto the balcony, away from the noise. | no | "Watch me." (bra on · Exhibitionism 20+) → `sleeve` | — |
| | | | "I'm not wearing one, Zo." (no bra · Exhibitionism 20+) → `already` | — |
| | | | "Dare me something else." (Corruption 20+ · `cocky_guy_met` · The cocky guy in Zoe's Living Room) → `kiss` | — |
| | | | "Not tonight, Zo." → `no` | — |
| `sleeve` | You reach up under Zoe's dress and unhook it at the back, and work one strap … | yes | "Ask for it back." → `mine` | Exhibitionism +3 (cap 79) · `zoe_has_bra` set · unequip plain bra · unequip sports bra |
| `already` | She looks at your chest for a long second, then laughs and leans on the rail … | no | "Laugh with her." → `mine2` | Exhibitionism +3 (cap 79) |
| `mine2` | There's a hot tub Saturday. | no | "Saturday." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 2 · `zoe_02_done` set · `party_house_invite` set · varies: `came_home_late` set, `late_party` set |
| `no` | She goes back inside and leaves the balcony door open behind her. | no | "Stay out on the balcony a minute." — 2 versions, by hour → Zoe's Living Room | Times you told Zoe no +1 · `zoe_balcony_refused` set · back in 7 days · varies: `came_home_late` set, `late_party` set |
| `kiss` | You take the beer out of his hand and set it on the counter. | yes | "Saturday?" → `saturday` | Corruption +3 (cap 39) |
| `saturday` | Zoe pulls you back out onto the balcony, flushed. | no | "Saturday." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 2 · `zoe_02_done` set · `party_house_invite` set · varies: `came_home_late` set, `late_party` set |
| `mine` | Zoe takes it out of your hand and tucks it in her back pocket. | no | "Saturday." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 2 · `zoe_02_done` set · `party_house_invite` set · varies: `came_home_late` set, `late_party` set |

**`zoe_02_balcony_curious`** — Zoe's Living Room · Fri 21:00-00:00 · Zoe there · needs Zoe's step = 1 · drinks boost off · 24h+ since `zoe_01_done` · Exhibitionism under 20 · Corruption 20+ · `cocky_guy_met` · The cocky guy in Zoe's Living Room · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `balcony` | Zoe pulls you out onto the balcony, away from the noise. | no | "Dare me something else." (Corruption 20+ · `cocky_guy_met` · The cocky guy in Zoe's Living Room) → `kiss` | — |
| | | | "Not tonight, Zo." → `no` | — |
| `no` | She goes back inside and leaves the balcony door open behind her. | no | "Stay out on the balcony a minute." — 2 versions, by hour → Zoe's Living Room | Times you told Zoe no +1 · `zoe_balcony_refused` set · back in 7 days · varies: `came_home_late` set, `late_party` set |
| `kiss` | You take the beer out of his hand and set it on the counter. | yes | "Saturday?" → `saturday` | Corruption +3 (cap 39) |
| `saturday` | Zoe pulls you back out onto the balcony, flushed. | no | "Saturday." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 2 · `zoe_02_done` set · `party_house_invite` set · varies: `came_home_late` set, `late_party` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`zoe_02_bra_through_the_sleeve` · `sleeve`** — 380 words · 8 counted: tits, tits, tits, nipple, nipple, tits, nipple, nipple · ceiling: Zoe's early column: tits, ass · **past the ceiling: nipples**

> You reach up under Zoe's dress and unhook it at the back, and work one strap down your arm and through the armhole of the dress, then the other.
>
> You reach up the back and unhook it, and work one strap down your arm and out through your sleeve, then the other.
>
> You reach up the back and unhook it, and work one strap down your arm and out through the armhole, then the other.
>
> There's no sleeve to work it through. You reach back, unhook it in one go, and peel it off your tits with the whole party on the other side of the glass.
>
> You reach up under Zoe's dress and drag the sports bra up, and work it off one arm at a time through the armholes of the dress.
>
> You drag the sports bra up off your tits under your top, and work it off one arm at a time, out through your sleeves.
>
> You reach up under the dress and drag the sports bra up off your tits, and work it off one arm at a time through the armholes.
>
> It takes forever. Zoe watches every second. When it slides out of your sleeve your nipples are hard in the cold air, two points anyone could see, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.
>
> It takes forever. Zoe watches every second. When it slides out through the armhole your nipples are hard in the cold air, two points anyone could see through the cloth, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.
>
> Your tits are bare on the balcony, your nipples hard in the cold air, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.
>
> It takes forever. Zoe watches every second. When it slides out through the armhole your nipples are hard in the cold air, two points anyone could see under her dress, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.
>
> Slower. Make the window wait for it.
>
> Zo, that guy is staring right at me.
>
> I know. Isn't it the best?

**`zoe_02_bra_through_the_sleeve` · `kiss`** — 203 words · 13 counted: kiss, cock, kiss, ass, tits, nipple, nipple, nipple, nipple, nipple, nipple, kiss, ass · ceiling: Zoe's early column: tits, ass · **past the ceiling: nipples**

> Fine. Kiss the cocky guy. Properly.
>
> You take the beer out of his hand and set it on the counter. He opens his mouth to say something, and you kiss it shut. Properly. Your tongue slides over his, slow, and his pushes back. Someone whoops, then the whole corner does. His hands drop to your ass and squeeze hard, one cheek filling each palm. He pulls you in until your tits press flat against his chest.
>
> Your nipples go hard under your top, and he feels them.
>
> Your nipples go hard under your dress, and he feels them.
>
> Your nipples go hard under your dress, and he feels them.
>
> Your nipples go hard through your bra, and he feels them.
>
> Your bare nipples go hard against his shirt, and he feels them.
>
> Your nipples go hard under your clothes, and he feels them.
>
> It's a dare. It doesn't count. Over his shoulder Zoe is biting her lip, eyes on your mouth. You kiss him deeper anyway, wet and open. Then you pull back first, breathing hard, lips wet. He grins down at you, both hands still full of your ass.
>
> Zoe. I owe you one.
>
> You owe her, not me. Hands off now.

**`zoe_02_balcony_curious` · `kiss`** — 203 words · 13 counted: kiss, cock, kiss, ass, tits, nipple, nipple, nipple, nipple, nipple, nipple, kiss, ass · ceiling: Zoe's early column: tits, ass · **past the ceiling: nipples**

> Fine. Kiss the cocky guy. Properly.
>
> You take the beer out of his hand and set it on the counter. He opens his mouth to say something, and you kiss it shut. Properly. Your tongue slides over his, slow, and his pushes back. Someone whoops, then the whole corner does. His hands drop to your ass and squeeze hard, one cheek filling each palm. He pulls you in until your tits press flat against his chest.
>
> Your nipples go hard under your top, and he feels them.
>
> Your nipples go hard under your dress, and he feels them.
>
> Your nipples go hard under your dress, and he feels them.
>
> Your nipples go hard through your bra, and he feels them.
>
> Your bare nipples go hard against his shirt, and he feels them.
>
> Your nipples go hard under your clothes, and he feels them.
>
> It's a dare. It doesn't count. Over his shoulder Zoe is biting her lip, eyes on your mouth. You kiss him deeper anyway, wet and open. Then you pull back first, breathing hard, lips wet. He grins down at you, both hands still full of your ass.
>
> Zoe. I owe you one.
>
> You owe her, not me. Hands off now.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 2 (heat 10-06) |
| the invite flag here | guess (fix 1, the flag check) |

> Changed 2026-11-02 (reader a3, older rows; DECISIONS 131; LO: "fix the older ones too"): in Zoe's dress the bra slides out through the armhole, not a sleeve.


## Changed 2026-11-03 (LO: "Go"; DECISIONS 133)

- Not the night of step 1: the balcony waits 24 hours after `zoe_01_done`.
- Only with a yes on screen: Daring (Exhibitionism 20) for the bra; or Curious (Corruption 20) under Daring with Jake's
 teammate at the party, where "Dare me something else." is the only yes (its own copy, `zoe_02_balcony_curious`).
- "You chickened out on me last time." now reads her no on this balcony (`zoe_balcony_refused`), not her no at the
 first party. The balcony's no moves `zoe_refused` +1.
- The card adds the goal "Reach Daring (Exhibitionism 20), or Curious (Corruption 20) with Jake's teammate at the party".
