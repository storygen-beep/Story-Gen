# craft/media.md — where pictures go, and what they ask for

Read this before you fill a card's `Media:` slot. A spot is a design decision; files come only after LO says "release ready" (SKILL.md, Always 6).

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C1261 | each spot costs a search, a shelf and a pick: put one where the player wants to look | P02–P06: 24 spots of "the room, empty" | a media spot | reader |
| C1267 | ask of each screen what the player should see that the words can't give; if nothing much, no spot | same | a media spot | reader |
| C1249 | the field's screen kinds: 41% of room screens in top games carry a picture | — (why a place may have one) | a media spot | note |
| C1250 | the room card stays bare in words; media goes to sex and talk | P02–P06 | a place is entered | reader |
| C1265 | a chore alone, a one-liner, a notice, a door, or a room or system menu (a place's buttons, the wardrobe, a shop list) gets no spot; a person's menu, opened from their face, is the exception: see C596 in `craft/people.md`. A place's `image` is not a spot of this kind: it is that place's card on the menu it's entered from (`v2.py:24764`) | P06's meals and sleep; P34's two readers split on Mom's menu picture as built and played in P42 (2026-11-24); P02b1-c1, where home_hall FAILED C1265 because its six room cards carry the six room pictures | a media spot | reader |
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
| C1238 | a picture matches its line on every visit | first_term's empty lounger, DECISIONS 258 (`games/first_term/DECISIONS.md:959`) | a media spot | reader |
| C1255 | one asset, one block | L126 | a media spot | reader |
| L97 | see `craft/walk-ins.md` |  |  |  |

## The engine (cited)

- A place's picture is one file, `image` on the `[[locations]]` row, with `image_search_queries` for the missing-media page (`v2.py:484`, `v2.py:493`).
- That file renders only as the place's card on the menu it is entered from: `_render_location_nav_card_body` is the only reader of `location_images` (`v2.py:24754`, `v2.py:24764`). The place's own screen never shows it.
- `pool_dir` names a folder; the game finds its files on disk and cycles them, one per visit (`v2.py:16382-16387`).
- `pool = N` is a target, not a manifest: it says how many files to aim for, so a half-filled pool reads "3 of 4" (`apps/common/media_blocks.py:18-20`). Left out, it is 4 (`apps/common/media_blocks.py:33`). That's the default L119 warns about, so always write it.

## The shape

1. **Sit on the payoff.** A spot goes right after the line where her body, his look or the act happens. The screen before it carries no spot.
2. **A place gets at most one picture: one file, tier 0, with her in it.** Never the empty room. The engine shows it as the place's card on the menu she enters it from, never on the place's own screen (`v2.py:24764`), so it is not a door or menu spot under C1265. If the place's own screen needs a picture of her, that picture is a media block in a scene there. The top games put a picture on 41% of room screens (C1249); CoT, the model for `craft/places.md`, puts none on its 126 location screens, so this rule comes from the field, not from CoT, and a picture of her in the place is what first_term's lounger fix asked for (DECISIONS 258, `games/first_term/DECISIONS.md:959`).
3. **Chores, doors, room and system menus, and solo everyday screens get none** (C1265). A person's menu gets their one picture (C596). A moment alone with her body is not one of them: a shower, dressing or undressing, the towel, bed, the mirror each get a picture of her (`craft/body-moments.md`; first_term_lean's P06 shower picture was "the shower running, steam on the glass"). An everyday picture that only repeats the line goes (first_term DECISIONS 251–252, `games/first_term/DECISIONS.md:952-953`).
4. **Size the pool by tier:** 4 for a repeatable explicit spot or a `_t4` body moment on a repeat (`craft/body-moments.md`), 2 for a `_t3` look on a repeat, 1 for everything else.
5. **A look shows what he sees.** Describe her, as seen from where he stands, with no man in frame.
6. **Does something happen in the picture?** Yes: a gif, with "gif" in the search words. No: a sharp still.
7. **The description:** her age, the place the scene is named for, what she's wearing on that visit, two or three plain search phrases.

## Worked example

Roles, not a world: a café as a place, the opening's lodger scene, and a repeatable act later.

**The café, its one place picture.** A place's picture is not a block: it is one file on the `[[locations]]` row, `image` with `image_search_queries` (`v2.py:484`, `v2.py:493`). There is no `pool` and no description field, so the search words carry her age and the place.

```toml
[[locations]]
id    = "cafe"
image = "places/cafe_t0.jpg"
image_search_queries = ["woman of 19 at a cafe window table with coffee", "young woman in a grey hoodie sitting in a cafe"]
```

She's in it, it's one file, and it's tier 0. Nothing moves, so it's a still. The player sees it as the café's card on the menu she walks in from, not on the café's own screen.

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

- "The room, empty, tier 0, her view" on every place. A place gets one picture with her in it. (P02–P06; DECISIONS 258)
- A spot on her meal or her bed when she's alone. A chore alone gets none. (P06; C1265)
- A second picture on a place, or a picture that only repeats the line. (DECISIONS 251–252)
- A pool with no `pool =`, which asks for 4. Write the number every time. (L119; `apps/common/media_blocks.py:33`)
- "A man looking at her in a towel." Write what he sees. (L120; C1281)
- A moving look tagged as a still. Does something happen? Then it's a gif. (L122; C1275)
- A picture on the line before the payoff. It sits on the line that says it. (L125; C1234)
- A picture with no age, or no named place. (L123; C1278, C1277)
