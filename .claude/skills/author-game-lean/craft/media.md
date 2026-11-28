# craft/media.md — where pictures go, and what they ask for

Read this before you fill a card's `Media:` slot. A spot is a design decision; files come only after LO says "release ready" (SKILL.md, Always 6).

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C1261 | each spot costs a search, a shelf and a pick: put one where the player wants to look | P02–P06: 24 spots of "the room, empty" | a media spot | reader |
| C1267 | ask of each screen what the player should see that the words can't give; if nothing much, no spot | same | a media spot | reader |
| C1249 | the field's screen kinds: 41% of room screens in top games carry a picture | — (why a place may have one) | a media spot | note |
| C1250 | the room card stays bare in words; media goes to sex and talk | P02–P06 | a place is entered | reader |
| C1265 | a chore alone (a work or upkeep screen whose payoff is a number, like pay), a one-liner, a notice (a posted sign or board, never her being noticed), a door (a button she clicks through, never a scene named after a door), or a room or system menu (a place's buttons, the wardrobe, a shop list) gets no spot; never a look at her, a touch on her, or sex she sees (C2204). A person's menu, opened from their face, is the exception: see C596 in `craft/people.md`. A place's `image` is not a spot of this kind: it is that place's card on the menu it's entered from (`v2.py:24930`) | P06's meals and sleep; P34's two readers split on Mom's menu picture as built and played in P42 (2026-11-24); P02b1-c1, where home_hall FAILED C1265 because its six room cards carry the six room pictures | a media spot | reader |
| C2204 | a scene that shows something sexual has a spot at its payoff: sex she sees `_t5`, skin or a touch on her `_t4`, a look at her `_t3`; a gif when something moves (C1275); a scene with none says why on its card (`No spot: <canvas> — <why>`), and the why is never C1265 | first_term_lean: 19 sexual scenes had no spot, their cards citing C1265 for a look ("a notice"), the storeroom ("a door"), a grope on the bus ("travel"), or nothing (LO, typed in main-lean 2026-11-27: "the group 2, gifs", "go ahead") | something sexual shows | script + media |
| C1262 | see `craft/body-moments.md` |  |  |  |
| C1234 | the clip sits on the beat the player is reading | L125 | a media spot | reader |
| L121 | media by kind of screen: every body moment, one everyday picture per scene; the every-screen overshoot was cut | first_term DECISIONS 251–252 cut solo everyday pictures that only repeat the line | a media spot | reader |
| L125 | a clip that opens its screen with the payoff spoils it | first_term's early-payoff clips | a media spot | reader |
| C1280 | pool size by spot: explicit repeat 4, a `_t4` body moment on a repeat 4 (LO, 2026-11-22), a `_t3` look on a repeat 2, everyday, person, room or once-seen 1; never the default by accident | L119 | a media spot | reader |
| L119 | default pools of 4 asked for 1,808 files | first_term DECISIONS 246 | a media spot | reader |
| C1281 | a look is written as what the looker sees, or the looker alone; never someone looking at her in the same frame | L120 | a media spot | reader |
| C1284 | a walk-in picture is what he sees: "Seen from a bathroom doorway: …" | L120 | a walk-in, a media spot | reader |
| L120 | "a man looking at her" frames can't be found, and two-person frames drew wrong searches | first_term DECISIONS 246–247, 253–254 | a media spot | reader |
| C1275 | a look where something happens asks for a gif (put "gif" in the search words); a held body or a room stays a still | L122 | a media spot | reader |
| C1274 | the tier suffix sets the format: `_t0` everyday, `_t3` a look, `_t4` skin, `_t5` sex, animated only | — | a media spot | note |
| C1278 | the description always gives her age | L123 | a media spot | reader |
| C1277 | name the place the scene is named for in every picture | L123 | a media spot | reader |
| C2207 | a place's picture is the place: nobody in it, and no person word in its search words | L173 | a media spot | script + media |
| C2208 | search words are tags, 8 words or fewer: the place or the act, one or two details, `gif` when something moves; never an age or number, "woman of", a camera direction, a "no ___", a name or a story word (the description carries those) | L173 | a media spot | script + media |
| C2209 | describe a picture that exists: one subject where it can be, a common act or pose; two people only where the act is the picture, never a choreographed gesture; the search words name no garment her clothes on that screen don't back | L173 | a media spot | reader |
| C1238 | a picture matches its line on every visit | first_term's empty lounger, DECISIONS 258 (`games/first_term/DECISIONS.md:959`) | a media spot | reader |
| C1255 | one asset, one block | L126 | a media spot | reader |
| L97 | see `craft/walk-ins.md` |  |  |  |

## The engine (cited)

- A place's picture is one file, `image` on the `[[locations]]` row, with `image_search_queries` for the missing-media page (read at `v2.py:500-519`).
- That file renders only as the place's card on the menu it is entered from: `_render_location_nav_card_body` is the only reader of `location_images` (`v2.py:24917`, `v2.py:24925`). The place's own screen never shows it. **A place with hours drops its picture while it is shut:** the card shows the placeholder and when it opens (`v2.py:24955-24963`, `setup.navDestOpenNow`). So the picture is only ever seen while the place is open.
- `pool_dir` names a folder; the game finds its files on disk and cycles them, one per visit (`v2.py:16533-16561`).
- `pool = N` is a target, not a manifest: it says how many files to aim for, so a half-filled pool reads "3 of 4" (`apps/common/media_blocks.py:18-20`). Left out, it is 4 (`apps/common/media_blocks.py:33`). That's the default L119 warns about, so always write it.

## The shape

1. **Sit on the payoff.** A spot goes right after the line where her body, his look or the act happens. The screen before it carries no spot.
2. **A place gets at most one picture: one file, tier 0, the place itself, with nobody in it** (C2207). The engine shows it as the place's card on the menu she enters it from, never on the place's own screen (`v2.py:24925`), so it is not a door or menu spot under C1265. **It shows only while the place is open** (`v2.py:24955-24963`). It is a photo of the room or the street, the way the old first_term's were, searched by the room and one or two details: "home kitchen interior daylight", "master bedroom interior double bed", "narrow front hallway terraced house coat hooks". No person word goes in its search words, because a person sends Google to stock models, and a place picture with someone in it says that someone is there at every hour it shows. If the place's own screen needs a picture of her, that picture is a media block in a scene there. *LO's choice* (LO, typed in main-lean 2026-11-28: "locations should be location photo not person. The old first term had good location photo."), reversing the rule from first_term's lounger fix (DECISIONS 258, `games/first_term/DECISIONS.md:959`) that put her in every place picture: in first_term_lean that rule drew 26 shelves that were 65% stock models (L173).
3. **Chores, doors, room and system menus, and solo everyday screens get none** (C1265). Each word means one thing: a chore is a work or upkeep screen whose payoff is a number; a door is a button she clicks through, never a scene named after a door ("The storeroom door" is a sex scene); a notice is a posted sign, never her being noticed. A look at her, a touch on her, or sex she sees is never one of them (rule 8). A person's menu gets their one picture (C596). A moment alone with her body is not one of them: a shower, dressing or undressing, the towel, bed, the mirror each get a picture of her (`craft/body-moments.md`; first_term_lean's P06 shower picture was "the shower running, steam on the glass"). An everyday picture that only repeats the line goes (first_term DECISIONS 251–252, `games/first_term/DECISIONS.md:952-953`).
4. **Size the pool by tier:** 4 for a repeatable explicit spot or a `_t4` body moment on a repeat (`craft/body-moments.md`), 2 for a `_t3` look on a repeat, 1 for everything else.
5. **A look shows what he sees.** Describe her, as seen from where he stands, with no man in frame.
6. **Does something happen in the picture?** Yes: a gif, with "gif" in the search words. No: a sharp still.
7. **The description and the search words are two different things.** The description says the picture in full: her age, the place the scene is named for, what she's wearing on that visit, and, for a look or a walk-in, where it's seen from (rules 5, C1281, C1284). The search words are two or three short tag lines, the words a picture is filed under on the sites that have it (C2208): the place or the act, one or two details, and `gif` when something moves (rule 6). Eight words or fewer. Never an age or a number ("woman of 18", "man 46"), a camera direction ("seen from behind a desk", "his view", "looking at the camera"), a "no ___" (Google adds the word, it can't leave it out), a name or a story word: a caption sentence is how only stock sites caption, so that's where it lands. A garment goes in only when that screen's clothing condition backs it (C2209). `check.py`'s `media` check reads every spot's and every place's search words. *Measured* (first_term_lean's find-media-v3 run, 2026-11-28: 74 slots searched the TOML's sentences as written; 49% of scene results and 82% of tier-0 results came from stock sites, L173).
8. **Every scene that shows something sexual gets a spot** (C2204), right after its payoff line (rule 1). The tier follows what happens: sex she sees is `_t5`, skin or a touch on her `_t4`, a look at her `_t3`, sized by rule 4, and a gif when something moves (C1275). The only way out is a reason written on the card, `No spot: <canvas> — <why>`, and C1265 is never the reason. `check.py`'s `media` check reads each card's `Does:` for `something sexual shows`, and each screen's own words for a look or a touch on her body (`SEXUAL_WORDS`: explicit words, eyes landing on her body, a hand that stays on her), and the build for a picture or clip block in that canvas. A first meeting keeps the person's face, `_t0`, as its picture: the player learns what he looks like there, and his look at her stays in the words (LO, typed in main-lean 2026-11-27: "A keep his face"). *LO's choice* (LO, typed in main-lean 2026-11-27: "the group 2, gifs", then "go ahead"), after first_term_lean shipped 19 sexual scenes with no spot; the field's media goes to sex and talk (C1250).
9. **Ask for a picture that exists** (C2209). One subject where it can be (L120, C1281), a common act or pose the sites tag, two people only when the act is the picture. A moment written as stage directions ("his thumb stroking the inside of her wrist, an envelope between their fingers"; "turned by her friend's hands so her ass faces the camera") has no picture anywhere: the search comes back with something nearby, and LO rejects the shelf (first_term_lean, seven such shelves, 2026-11-27). Write the nearest picture that is filed somewhere, and let the words carry the rest.

## Worked example

Roles, not a world: a café as a place, the opening's lodger scene, and a repeatable act later.

**The café, its one place picture.** A place's picture is not a block: it is one file on the `[[locations]]` row, `image` with `image_search_queries` (`v2.py:513`, `v2.py:512`). There is no `pool` and no description field. It is the café itself, nobody in it.

```toml
[[locations]]
id    = "cafe"
image = "places/cafe_t0.jpg"
image_search_queries = ["small cafe interior window tables", "cosy coffee shop counter daylight"]
```

It's the place, it's one file, and it's tier 0. Nothing moves, so it's a still. Its search words are the room and two details: no person, no age. The player sees it as the café's card on the menu she walks in from, not on the café's own screen.

**The temptation screen, one spot, right after the look** (screen 5 of `craft/opening.md`):
> His eyes drop to your wet thighs, where the towel ends, and climb slow to your chest.

```toml
[[canvases.nodes.blocks]]
type = "image"
props = { description = "Seen from a landing: a woman of 19 in a short white towel outside a bathroom door, legs wet, the knot under her arm slipping. No man in frame.", search_queries = ["woman short towel outside bathroom door gif", "towel slipping wet legs hallway gif"], pool_dir = "look/landing_towel_t3", pool = 1 }
```

It's seen once, so the pool is 1. The knot slips, so it's a gif.

**The same scene's other screens:** the setup, the landlord, the start choice, the bathroom and the card get no spot, because nothing on them is a body moment. The kitchen hand-over gets none either: the kitchen's place picture shows only as its card on the menu she enters the kitchen from, not on the kitchen's screen.

**A repeatable act at a later stage, one spot per beat:**
> He pulls the towel off you and you let it go. *(beat 1: a clip right after this line)*
> His mouth is on your tit before you can say his name. *(beat 2: its own clip, its own pool)*

Each beat is `_t5`, video, `pool = 4`, because the player comes back to it.

## Not this

- A sexual scene with no spot because its card called it a door, a notice or travel: first_term_lean's storeroom ("The storeroom door"), the five "she gets noticed" scenes ("a look scene… C1265"), the grope on the packed bus ("travel screens get none"). Rule 8; C2204.

- A spot on a place's own screen showing the room, empty. The place's picture is its card on the menu (rule 2); a picture on its screen is a scene's. (P02–P06)
- A place picture with her, or anyone, in it: "woman of 18 eating toast at a small family kitchen counter". The place is the picture. (L173; C2207)
- Search words written as a caption: "seen from behind a big desk: woman of 18 standing in the doorway of a college dean's office, waiting", "man 46 armchair living room remote tv light", "girl at a row of sinks, no phone". Tags, eight words or fewer. (L173; C2208)
- A picture nobody has made: a choreographed gesture between two people. Ask for the nearest one that is filed somewhere. (L173; C2209)
- Search words that dress her: "braless tank top" on a screen where she's in a t-shirt and jeans. (first_term_lean P49 reader, 2026-11-28; C2209)
- A spot on her meal or her bed when she's alone. A chore alone gets none. (P06; C1265)
- A second picture on a place, or a picture that only repeats the line. (DECISIONS 251–252)
- A pool with no `pool =`, which asks for 4. Write the number every time. (L119; `apps/common/media_blocks.py:33`)
- "A man looking at her in a towel." Write what he sees. (L120; C1281)
- A moving look tagged as a still. Does something happen? Then it's a gif. (L122; C1275)
- A picture on the line before the payoff. It sits on the line that says it. (L125; C1234)
- A picture with no age, or no named place. (L123; C1278, C1277)
