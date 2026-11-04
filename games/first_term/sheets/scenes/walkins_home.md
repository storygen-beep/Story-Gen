# [READY] Scenes — the walk-ins at home (B1-B8)
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, LO's answers: Mark covers while her Corruption is under 20 in walkin_kitchen_mark and both walkin_tv_mark, "Good girl." reworded (E, A); signed by LO 2026-11-04.

> New 2026-11-03 (third alignment pass): written from the build, for LO to read and sign. The plan is the signed
> heat proposal, `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`, part B (signed 2026-11-03, DECISIONS 147),
> built in DECISIONS 148 and 152. Nothing here is new design; where the build differs from the proposal, the
> difference is named.

## How every walk-in works, as built

| row | answer |
|---|---|
| where it starts | she clicks a solo activity; on entry the game rolls, and a hit shows the walk-in instead |
| odds | 0.25 · 0.35 · 0.45 by her meter's band (under 20 · 20–39 · 40+) |
| louder odds | 0.5 · 0.7 · 0.9 while the shower door is unlocked (C4) or the TV is loud (C2) |
| screen 1 | the moment: his Lust +2 on its only button, once a day per walk-in |
| screen 2 | her answer: the cover pays 0; one bolder button per band pays her +1, capped at the band's top |
| no meter | Kayla, Laura: nothing of theirs moves; a flag records it |
| once a day | each walk-in sets its own `walkin_*_today`, cleared at midnight |
| a miss | her activity, as it is today |

Different from the proposal: the odds rise with her band (the proposal had 0.25 flat). B2's "Push back into
him." is Bold, cap 59 (LO confirmed, DECISIONS 151). Each Saturday walk-in with Mark rolls in the 15 minutes
before his row starts (DECISIONS 152).

---

## B1 · the shower (`bathroom_shower`)

### `walkin_shower_ryan`

| row | answer |
|---|---|
| who · when | Ryan, from his room · Sun–Thu 19:00–00:00 · Sat, Sun 07:30–14:00 |
| want | his: he stops in the door and looks |
| next step | her bolder answer at the next Exhibitionism band |
| hook | `ryan_walked_in_shower` is set; nothing reads it this release |
| screen 1 | "He's seen you." · his Lust +2 |
| her answers | "Grab the towel." 0 · "Don't grab it straight away." +1, cap 19 · "Keep washing." (Daring) +1, cap 39 · "Turn round." (Showing) +1, cap 59 |
| every way out | "Dry off." · hygiene +50 |

### `walkin_shower_kayla`

| row | answer |
|---|---|
| who · when | Kayla, Friday 18:00–22:00, Ryan in his room · after she has met Kayla |
| want | Kayla's: she looks her over while she pees |
| next step | her bolder answer at the next band |
| hook | `kayla_saw_her`: Kayla has a line in Ryan's room for 48 hours |
| screen 1 | "She sits down to pee." · nothing moves |
| her answers | the same four as Ryan's, the same pays |

### `walkin_shower_mark`

| row | answer |
|---|---|
| who · when | Mark, from the garage · Saturday 14:00–17:00 · after `mark_saw_her` · Laura not in the bathroom |
| want | his: he doesn't look away |
| next step | her bolder answer at the next band |
| hook | `mark_walked_in_shower` is set; nothing reads it this release |
| screen 1 | "He's seen you." · his Lust +2 |
| her answers | the same four, the same pays |

C4, "Leave the door unlocked.", sits on the shower itself and raises these odds (see the bathroom sheet).

## B2 · the kitchen (`kitchen_breakfast`, `kitchen_coffee`)

### `walkin_kitchen_ryan`

| row | answer |
|---|---|
| who · when | Ryan, down from his room · Saturday 07:30–08:15 · Sunday 07:30–10:00 |
| want | his: morning wood against her ass as he reaches past |
| next step | "Push back into him." at Bold |
| hook | `ryan_brushed_kitchen` is set; nothing reads it this release · every answer names next weekend's mug: "Next weekend he'll come in for a mug again." (step aside, don't move; pass 4 reader) · "Next weekend I'm coming in for that mug again." (push back) |
| screen 1 | "He freezes." · his Lust +2 · he "comes in from the hall" (Q7, one hall) |
| her answers | "Step aside." 0 · "Don't move." +1, cap 19 (cap 39 from Curious) · "Push back into him." (Bold) +1, cap 59 |
| every way out | "Drink your coffee." |

### `walkin_kitchen_mark`

| row | answer |
|---|---|
| who · when | Mark, down from bed · Saturday 08:15–08:30 · after `mark_saw_her` |
| want | his: his hand flat on her hip to reach the coffee jar |
| next step | "Push back into him." at Bold |
| hook | `mark_brushed_kitchen` is set; nothing reads it this release |
| screen 1 | "His hand stays." · his Lust +2 |
| her answers | the same three as Ryan's, the same pays |

## B3 · the TV, channel 5 (`living_tv`)

| canvas | who · when |
|---|---|
| `walkin_tv_mark_garage` | Mark, in from the garage · Mon, Tue, Thu, Fri 21:30–22:00 · after `mark_saw_her` |
| `walkin_tv_mark_kitchen` | Mark, in from the kitchen · Wednesday 21:30–22:00 · after `mark_saw_her` |
| `walkin_tv_ryan` | Ryan, down from his room · Sat, Sun 13:30–14:00 |
| `walkin_tv_laura` | Laura, in from the kitchen · Sunday 21:30–21:58 |

| row | answer |
|---|---|
| want | his: he stops in the doorway and watches the screen with her |
| next step | "Leave it on." from Curious |
| hook | Mark: `mark_caught_ch5` gives him a line in his late hub for 24 hours · Ryan, Laura: a flag nothing reads yet |
| screen 1 | "He's seen the screen." · his Lust +2 · Laura: "She's seen the screen." · nothing moves |
| her answers | "Turn it off." 0 · "Don't reach for the remote yet." +1, cap 19 · "Leave it on." (Curious) +1, cap 39 |
| Laura | one answer only: "Turn it off." · no pay |
| every way out | "Get up." (after "Leave it on.": "Turn it off.") |

C2, "Turn the sound up.", raises these odds (see `living_tv_channels.md`).

## B4 · the laundry (`garage_laundry`)

| canvas | who · when |
|---|---|
| `walkin_laundry_mark` | Mark, in from the kitchen · Mon, Tue, Thu, Fri 18:45–19:00 · after `mark_saw_her` |
| `walkin_laundry_mark_sat` | Mark · Saturday 08:45–09:00 · after `mark_saw_her` |

| row | answer |
|---|---|
| want | his: he stops in the doorway while she's bent at the drum |
| next step | the laundry tease ladder, one button per stage |
| hook | `mark_walked_in_laundry` is set; nothing reads it this release |
| screen 1 | "He stops in the doorway." · his Lust +2 |
| her answers | "Load it and go." 0 · "Leave your basket on top." (Curious) his Lust +2 · "Bend for the bottom drum." (Curious, Daring) his Lust +3, her Exhibitionism +1, cap 39 · "Wash what you're wearing." (Bold, Showing) his Lust +4, both of hers +1, cap 59 · "Leave it for later." |
| where they go | into the built tease screens (`mark_laundry_teases.md`) |

## B5 · the hall mirror (`hall_mirror`)

| canvas | who · when |
|---|---|
| `walkin_mirror_ryan` | Ryan, from his room · Sat, Sun 07:30–14:00 · Sun–Thu 19:00–00:00 |
| `walkin_mirror_mark` | Mark, coming up to bed · Mon–Sat 01:30–02:00 · after `mark_saw_her` · Laura not in the hall |

| row | answer |
|---|---|
| want | his: he looks at her in the mirror |
| next step | "Stay at the mirror." pays to the next band's top |
| hook | `ryan_saw_mirror` / `mark_saw_mirror`; nothing reads them this release |
| screen 1 | "He's looking." · his Lust +2 · it also sets `home_event`: one hall accident a day |
| her answers | "Go to your room." 0 · "Stay at the mirror." +1, cap 19 · 39 · 59 by her band |
| the way out | "Go on." |

## B6 · Laura's wardrobe (`master_wardrobe`)

### `walkin_wardrobe_laura`

| row | answer |
|---|---|
| who · when | Laura, from the bathroom · Saturday 16:45–17:00 |
| want | Laura's: she sees her daughter in her dress |
| next step | none: the good-mom branch, no heat |
| hook | `laura_saw_wardrobe` is set; nothing reads it this release |
| screen 1 | "She's seen the dress." · nothing moves |
| her answer | "Leave her to it." · no pay |

### `walkin_wardrobe_mark`

| row | answer |
|---|---|
| who · when | Mark, up from the bar · Saturday 21:45–22:00 · after `mark_saw_her` |
| want | his: he stares at her in Laura's lingerie and doesn't touch |
| next step | "Let him look." pays to the next band's top |
| hook | `mark_saw_lingerie` is set; nothing reads it this release |
| screen 1 | "He stops in the doorway." · his Lust +2 · he says nothing (no row for a line before 22:00) |
| her answers | "Cover up." 0 · "Let him look." +1, cap 19 · 39 · 59 by her band |
| the way out | "Get changed. Go." |

## B7 · Ryan's things (`ryan_things`)

### `walkin_things_ryan`

| row | answer |
|---|---|
| who · when | Ryan, up from dinner · Sun, Mon, Tue, Thu 18:45–19:00 |
| want | his: she's holding his half-gone box of condoms |
| next step | "Hold it up. 'Explain this.'" |
| hook | `ryan_things_found`: his things read differently after |
| screen 1 | "He's caught you." · his Lust +2 |
| her answers | "Put it back." 0 · "Hold it up. 'Explain this.'" +1, cap 19 · then "Leave him to it." |

### `walkin_things_kayla`

| row | answer |
|---|---|
| who · when | Kayla, arriving with him · Friday 17:45–18:00 · after she has met Kayla · Ryan not in the room |
| want | Kayla's: "Snooping?" |
| next step | none |
| hook | `ryan_things_found`; `kayla_caught_her` is set, nothing reads it this release |
| screen 1 | "She's seen you." · nothing moves |
| her answer | "Put it back." · no pay |

## B8 · the front step (`front_step`)

### `walkin_step_vance`

| row | answer |
|---|---|
| who · when | Vance, from his porch · every day 18:00–21:00 · after she has met him · not in jeans or leggings |
| want | his: he stops at the gate and looks at her legs |
| next step | "Stretch your legs out." at Daring |
| hook | `vance_saw_step` is set; nothing reads it this release |
| screen 1 | "He stops at the gate." · his Lust +2 |
| her answers | "Knees together. Go in." 0 · "Leave them." +1, cap 19 · "Stretch your legs out." (Daring) +1, cap 39 · then "Go back in." |

Different from the proposal: B8's Jake (early for a date) was left out, because his rows don't put him there
at that hour (DECISIONS 148).

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `walkin_shower_ryan` · `answer` | 119 | 4: tits ×2, naked, cock | Ryan's middle column | written out below |
| `walkin_shower_kayla` · `answer` | 72 | 3: tits ×2, pussy | Kayla: no column on SP2; crude words used: pussy, tits | written out below |
| `walkin_shower_kayla` · `k_cov` | 53 | 4: tits ×3, nipples | Kayla: no column on SP2; crude words used: tits | written out below |
| `walkin_shower_kayla` · `k_sho` | 59 | 3: ass ×2, nipples | Kayla: no column on SP2; crude words used: ass | written out below |
| `walkin_shower_mark` · `answer` | 165 | 3: naked, tits, pussy | Mark's middle column; also pussy | written out below |
| `walkin_kitchen_ryan` · `r_stay` | 62 | 3: cock, ass, nipples | Ryan's middle column; also nipples | written out below |
| `walkin_tv_mark_garage` · `moment` | 83 | 4: cock, tits, thrust, moans | Mark's middle column | written out below |
| `walkin_tv_mark_kitchen` · `moment` | 73 | 4: cock, kisses, tits, moaning | Mark's middle column | written out below |
| `walkin_tv_mark_kitchen` · `m_gg` | 63 | 3: licks, nipple, nipples | under Mark's columns; also nipples | written out below |
| `walkin_tv_ryan` · `moment` | 72 | 3: tits, ass, moans | Ryan's early column | written out below |
| `walkin_tv_ryan` · `answer` | 58 | 3: cock, moans, tits | Ryan's middle column | written out below |
| `walkin_tv_ryan` · `r_cur` | 77 | 3: moans, cock, fuck | Ryan's late column | written out below |
| `walkin_mirror_ryan` · `answer` | 200 | 7: tits ×2, ass ×2, naked, pussy, nipples | Ryan's early column; also nipples, pussy | written out below |
| `walkin_mirror_mark` · `answer` | 208 | 7: tits ×2, ass ×2, naked, pussy, nipples | Mark's middle column; also nipples, pussy | written out below |
| `walkin_wardrobe_mark` · `answer` | 222 | 7: tits ×4, nipples ×3 | Mark's middle column; also nipples | written out below |
| `walkin_wardrobe_mark` · `m_look` | 143 | 3: nipples ×2, tits | Mark's middle column; also nipples | written out below |

The screens not written out above, as built:

- `walkin_shower_ryan` · `answer` · 119 words · 4 counted:

> You're naked and wet three feet from him. His eyes go straight to your tits, then down, all the way down, and come back up slow. He goes red to the ears. He turns side-on, too late. The front of his shorts is already tenting. Shit. Sorry. I didn't. The lock. I didn't know you were in here. Well, now you know. He doesn't go red. He leans on the door frame and keeps looking at your tits. His cock is hard in his shorts, and he doesn't turn it away. Don't mind me. I'm just getting my toothbrush. Your toothbrush is on the sink, Ryan. You left the door unlocked for this. For somebody to walk through it.

- `walkin_shower_kayla` · `answer` · 72 words · 3 counted:

> She pees with the shower running and looks you over the whole time, from your wet tits down to your pussy and back up. Oh, hi. Don't mind me. I couldn't hold it. She flushes and doesn't leave. She leans on the sink and looks at your tits like she's comparing. Look at you, step-sister. And you're in my bathroom. You left the lock off. Somebody was always going to use it.

- `walkin_shower_kayla` · `k_cov` · 53 words · 4 counted:

> You don't grab it straight away. You let her look a second longer, your nipples hard, the water running off your tits. Nice tits. Ryan never said. Why would Ryan say anything about my tits? Good question. I'll ask him. She winks and goes. You grab the towel with your face on fire.

- `walkin_shower_kayla` · `k_sho` · 59 words · 3 counted:

> You turn round under the water and give her your wet ass. Kayla laughs, low. Oh, you're trouble. Does he know you're trouble? Who? Don't play dumb with me, babe. Shake that ass at him and you'll have me to deal with. She smacks the door frame on her way out. You stand there wet and grinning, nipples hard.

- `walkin_shower_mark` · `answer` · 165 words · 3 counted:

> You're naked under the water. His eyes go to your tits and stay there. Then lower, to your pussy, and they stay there too. Then he catches himself. He turns to the sink, hard, and puts his eyes on the tiles above the tap. He turns his hip to you, so the front of his jeans faces the wall. Sink's the only one with hot water. I'll be one minute. Don't. Don't what? Don't stand there like that. Wash, girl. He doesn't look away. He turns the tap on at the sink and scrubs his hands, and in the mirror his eyes are on you the whole time. Sink's the only one with hot water. Don't mind me. He doesn't look away. He turns the tap on at the sink and scrubs his hands, and in the mirror his eyes are on you the whole time. Don't stop on my account. You left the lock off, and he walked right in. You knew he might.

- `walkin_kitchen_ryan` · `r_stay` · 62 words · 3 counted:

> You don't move. You stand there with his cock pressed into your ass and let him feel you not moving. Your nipples go hard. @player.nickname. You're. You're not moving. Neither are you. He breathes out, shaky, and steps back. He takes his mug back to his room and doesn't look at you once. He felt you stay. He knows you felt him.

- `walkin_tv_mark_garage` · `moment` · 83 words · 4 counted:

> You drop onto the couch and thumb the TV on, and it comes up on channel 5, where whoever had it last left it. A woman on her knees on a bed, a man behind her, his cock sliding in and out of her. Her tits swing with every thrust. You left the sound up from earlier. Her moans fill the room and carry out to the garage door. The sound's low, at least. You look at the hall door, quick. Mark walks in from the garage with a beer and stops behind the couch.

- `walkin_tv_mark_kitchen` · `moment` · 73 words · 4 counted:

> The TV's on with nobody watching it, stuck on channel 5. You're on the couch before you see what's on it. Two women on a couch with one man between them. One rides his cock while the other one kisses her tits. You left the sound up from earlier. The moaning carries over the kitchen fan. The sound's low, at least. You look at the hall door, quick. Mark walks in from the kitchen with a beer and stops behind the couch.

- `walkin_tv_mark_kitchen` · `m_gg` · 63 words · 3 counted:

> You don't reach for the remote. Not yet. On screen the girl on top comes, loud, and the other one licks her nipple. Mark's hands come off the back of the couch, and he catches himself and looks at the ceiling. Your face is burning, and your nipples are tight. Your mother doesn't watch this one. I'm not my mother. I know. Turn it off, @player. You turn it off. He lets his breath go and looks anywhere but at you.

- `walkin_tv_ryan` · `moment` · 72 words · 3 counted:

> You flop down, hit the power button, and there it is, channel 5, the last thing anybody had on. A man flat on his back and a girl riding him, her tits bouncing, his hands full of her ass. You left the sound up. Her moans go all the way down the hall. The sound's low, at least. You look at the hall door, quick. Ryan comes in from the hall for the TV and stops in the doorway.

- `walkin_tv_ryan` · `answer` · 58 words · 3 counted:

> He looks at the screen. She drops down on the man's cock, and she moans. Then he looks at you. Seriously, @player.nickname? It's the middle of the day. And? He goes red, but he doesn't go back to his room. His eyes go back to her tits on the screen, and he shoves his hands in his pockets.

- `walkin_tv_ryan` · `r_cur` · 77 words · 3 counted:

> You leave it on. Ryan sits down on the far end of the couch, very straight. On screen he takes her from behind, hard, and she moans every time his cock drives in. Ryan's knee bounces. His hand sits on his thigh, an inch from the bulge in his shorts. You're wet, and you don't move either. We're not doing this. We're not. Turn it off. You turn it off. The remote's right there. Don't. Just. Fuck.

- `walkin_mirror_ryan` · `answer` · 200 words · 7 counted:

> You're in a towel. From his doorway, in the glass, his eyes go to the knot over your tits, then down your bare thighs. You're naked. From his doorway, in the glass, his eyes go straight to your tits, then down to your pussy, and stay. Bra and panties. From his doorway, his eyes go down your back to your ass in your panties. Nothing under your skirt, and it's short. From his doorway, his eyes go to the backs of your thighs and up, to where the hem stops. Your skirt is short. From his doorway, his eyes go up the backs of your bare thighs to your hem. No bra. From his doorway, in the glass, his eyes find your nipples through your top. You're dressed. From his doorway, his eyes go down your back to your ass anyway. Half dressed. From his doorway, his eyes go to what's missing first. He catches you catching him in the glass. He goes red and looks at the carpet. Is the bathroom free? Since when do you ask? Since now. Is it? He catches your eyes in the glass and doesn't look away. Looking good, @player.nickname. Going somewhere? Not anymore.

- `walkin_mirror_mark` · `answer` · 208 words · 7 counted:

> You're in a towel. From behind you, in the glass, his eyes go to the knot over your tits, then down your bare thighs. You're naked. From behind you, in the glass, his eyes go straight to your tits, then down to your pussy, and stay. Bra and panties. From behind you, his eyes go down your back to your ass in your panties. Nothing under your skirt, and it's short. From behind you, his eyes go to the backs of your thighs and up, to where the hem stops. Your skirt is short. From behind you, his eyes go up the backs of your bare thighs to your hem. No bra. From behind you, in the glass, his eyes find your nipples through your top. You're dressed. From behind you, his eyes go down your back to your ass anyway. Half dressed. From behind you, his eyes go to what's missing first. His hands close into fists at his sides. Then he catches himself. He looks down at the hall carpet, at his own feet, anywhere but the glass. Bit late to be standing there, @player. Bed. Night, Mark. Night. He stands there and doesn't pretend he's doing anything else. Bit late to be standing there, @player.

- `walkin_wardrobe_mark` · `answer` · 222 words · 7 counted:

> He smells of beer. He stands in his own bedroom doorway with his keys still in his fist and looks at you in his wife's bra. His eyes go to your tits in the black lace, to your nipples through it. Then he catches himself and looks at the wall above your head, hard, and keeps them there. He doesn't take one step into the room. He doesn't say a word. His jaw works like he's going to tell you to take it off, but he doesn't. His eyes go to your tits in the black lace, to your nipples through it, and stay there. Then down your stomach, slow, and back up. The front of his jeans fills, but he doesn't take one step into the room. He doesn't say a word. His eyes go to Laura's open drawer and back to your tits, and his jaw works like he's going to tell you to take it off, but he doesn't. His eyes go to your tits in the black lace, to your nipples through it, and stay there. Then down your stomach, slow, and back up. The front of his jeans fills, but he doesn't take one step into the room. He doesn't say a word. He leans on the door frame to look longer, and he wets his lips.

- `walkin_wardrobe_mark` · `m_look` · 143 words · 3 counted:

> You don't cover up. You can't make your arms move. You stand there facing him in his wife's bra with your face on fire and your nipples hard through her lace. Mark. Say something. Please. *Cover up. Cover up. You don't.* You don't cover up. You turn round to face him, drop your hands to your sides, and let him look at you in his wife's bra. Does it look better on her, Mark? Or on me? He looks. A long time. At your tits in the lace, your nipples hard through it. His keys bite into his fist, but he still doesn't come in. He breathes out hard through his nose. Then he steps back into the hall and pulls the door to without a word, and leaves you to get changed. He'll think about this bra every time she wears it.
