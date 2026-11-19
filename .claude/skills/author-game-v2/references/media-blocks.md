# Media blocks — which screens get one, and where it goes

A media block is the picture or clip spot on a screen: a `type = "image"` or `type = "video"` block whose `props`
carry `description`, `search_queries`, and either `pool_dir` (a folder the engine cycles, one file a visit) or `file`.
The author writes the block when the scene is written. The file itself comes later, at "release ready?": an empty
pool renders nothing and goes on the missing-media page (`generators/v2.py`, `missing_media.append` in the pool
renderer). So a block costs nothing to write early, and a screen that should have one and was written without it
ships without a picture. But a block is not free later: each one is a search, a shelf to review and a pick. Put
one where the player wants to look, and leave the rest plain.

Taught from first_term's release 1 pass (LO, 2026-11-12: "We have not been mentioning the media blocks at all"),
where 24 of 167 shipped screens had media and the everyday screens had none.

## What gets a block

| the screen | the block | top games, share of screens with a picture |
|---|---|---|
| a body moment: a look, something shows, sex, her own hand | a clip (or still) right after the line that says it, on the same screen. Always | sex 86–92% |
| a person's hub (his room, her kitchen) | one picture of that person, first on the hub's first screen, and only one: a stock photo of a named person is a new face every time | rooms/hubs 41% |
| a one-time step or first meeting | one picture or clip on its key line | — |
| a moment with a person in it (a walk-in, an event, a late entry, a talk with someone there) | one picture of the moment, when the person or what they do is worth seeing | talk 64% |
| a find that matters (the condoms in his drawer, her hidden dresses, his locked box) | one picture of the thing | — |
| a chore or errand she does alone (breakfast, dishes, a nap, the library desk, the park bench) | none: the line says it, a picture only repeats it | ordinary 36% |
| a one-liner, a notice, a stat line, a menu, a door | none | one-liners 21% |

The right-hand column is the study in `register.md` "The table" (27 shipped sandboxes, 54,630 screens). It is
what the field does, not a quota.

## By kind of screen, not every screen
Count by screen and sort by kind. A choice opens a new screen and the picture before it is gone, so a scene is not
"done" because its first screen has one. But not every screen wants one either: top games put pictures where the
payoff is (sex, a person, a reveal) and leave rooms, errands and stat lines mostly plain. A plain chore screen is
the field agreeing with itself, not a gap, and when the plain screens stay plain the player feels it when a
picture does appear.

Ask for each screen: what should the player SEE here that the words can't give? Her body, a person, something she
finds. If the answer is nothing much, it gets no block.

Taught from first_term twice. On 2026-11-12, 320 of release 1's 448 screens had no block, and the fix asked for
"every screen" (LO: "Mark in living room also didn't have media for all interaction with him"). By 2026-11-18 that
had overshot to 439 of 446 screens (98%), with 19 pictures on Laura's kitchen hub alone. LO asked "Does all scenes
needs media blocks?? How top games do it??", and 193 everyday pictures went (DECISIONS 251, 252). That left
release 1 at 55% of screens, near the field by kind except ordinary screens (body looks keep those higher).

## The rules

1. **On the line, not the top.** A node is one screen, and its blocks render in order. A clip placed right after the
   line it shows appears right there. A clip at the top illustrates only what comes first (register.md, "The clip
   rides the beat"). In a cascade, put it in the beat's own `blocks`.
2. **The picture agrees with the words on every visit.**
   - When a screen's text changes with what she wears (towel, naked, underwear), each version gets its own block
     inside its own group.
   - A block never sits where it would show on a visit its line doesn't render on. If a line comes in many
     versions (alternate entries of a pool, conditional variants), no single block can follow it truthfully: put
     the block on a line every visit shares, or leave it out and say so.
3. **Two body moments, two clips.** A scene where she bends over the washer and he gets hard carries two clips on
   one screen: hers after her line, his after his. Each has its own pool. Both render, in order.
4. **One asset, one block.** No two blocks name the same pool or file (gate `one asset, one block`). A block written
   once in a helper that builds several canvases gets a name per canvas (`own_media`, or a per-canvas suffix).
5. **A repeatable explicit screen cycles.** It uses `pool_dir`, never a single `file` (gate `repeatable explicit
   media cycles`).
6. **The tier is in the name, and it sets the format** (find-media `tier_format_check.py`):
   - `_t0` everyday, a still or a gif
   - `_t3` a look, a towel, cleavage, a still or a gif (`tier_format_check.py` allows `.gif` at `_t0`-`_t3`;
     a `.gif` in a picture pool renders as an animated `<img>`). **Ask one question: does something happen in
     the picture?** If yes, it asks for a gif. She walks, bends, sits up, tucks a towel, pulls a robe in,
     slips past, stretches, checks herself in a mirror, writes or draws, looks up when caught. A man reaches past
     her or opens a door. Steam rolls out, water runs. Read the description's verbs, not a keyword list. If she
     is holding still and the picture is her body (standing at a mirror, legs on a couch, lying down, sitting on
     a step), or it shows a room, someone asleep, a touch that just holds, or only eyes moving, it stays a still.
     A sharp still shows a held body better than a wobbling gif. Put `gif` in the search words; the name can
     stay `.jpg` or a picture pool (the engine finds the file whatever its extension, `v2.py`
     `_find_media_file`), and find-media-v3 reads `gif` in the search words as animated. Taught from
     first_term, where 51 moving looks asked for stills across two passes (LO, 2026-11-18).
   - `_t4` skin, a still or a clip
   - `_t5` sex or masturbation, animated only
   - `sex/` for `_t4`/`_t5`; the gates count `_t4`, `_t5` and `sex/` as explicit
7. **Describe it for the search, and read it as an adult.** `description` says what the frame shows, with the
   people's ages when they matter (every person is an adult). `search_queries` are two or three plain search
   phrases. No gate reads either one. The media review does.
   - **Name the place the scene is named for.** A scene called "check your clothes in the hall mirror" puts the
     mirror in every one of its pictures, not only "in the hall".
   - **Always give her age.** A picture without one lets the search write `milf`.
   - **A mirror picture says "No phone."** Without it, the search writes `selfie`.
   Taught from first_term (LO, 2026-11-18). The hall-mirror towel and naked pictures said only "in a house
   hallway", and the search found women walking naked down hallways.
8. **How many files a spot holds.** A pool aims for 4 files unless it says otherwise (`DEFAULT_POOL_TARGET`,
   `apps/common/media_blocks.py`), and the engine starts every pool at its first file, so set `pool = N` by what
   the spot needs:

   | the spot | files |
   |---|---|
   | explicit (`_t4`/`_t5`/`sex/`) on a repeat screen | 4, the default (gate `repeatable explicit media cycles`) |
   | a `_t3` look on a repeat screen | `pool = 2` |
   | an everyday spot, a person, a room, a thing | `pool = 1` (or a single `file`) |
   | anything on a screen seen once | `pool = 1`: a second file would never show |

   Never leave the default by accident. Taught from first_term (LO, 2026-11-18: "they dont need 4 shelfs they
   can just be one"), where the every-screen pass left 452 pools at 4 and release 1 asked for 1,808 files; sized
   by this table it asked for 740.
9. **A picture you can find.** One subject per frame. A look is written as what the one looking sees ("her bare
   legs walking past a couch", "down her low-cut top from the next seat"), or as the looker alone ("a shy woman in
   a doorway, blushing"), never as someone looking at her: two people and a glance in one real photo barely
   exists, and the line already says who looks. The looker can be a woman: first_term's Biology TA picture
   ("her eyes running down a student") sent the harvest to "lesbian milf … seduction" searches for a shy, clothed
   glance (LO, 2026-11-18). Taught from first_term's 56
   glance spots (LO, 2026-11-18: "these are very very hard to find"), and 17 more a keyword scan missed: test who
   is in the frame, not whether the line says "looks". Keep a man in frame only where the touch is the picture.
10. **The name is the shelf key.** The harvest stocks a spot's shelf, and records LO's pick, under the spot's
   name. Once a spot has either, don't rename it (adding an extension is a rename): change how many files it
   holds with `pool = N`. A block with an authored `id` keeps its shelf when its path moves
   (`apps/common/media_blocks.py`, `block_slot_key`).
11. **No harvest while writing.** Writing a block never means searching or downloading. The files come when the
   person who owns the game asks for them.

## How it is checked
- `lint · a screen without media`: our share of screens with a picture by kind, beside the top games' share, and
  only the bare screens the table above wants a picture on: a sex screen with no clip, a one-time scene with no
  picture anywhere, a person's hub opening bare. A bare chore screen is not listed. It never fails; read it each
  release.
- `an explicit beat carries a clip`: at least 50% of explicit beats carry their own clip. Its report lists every
  screen still missing one, so read the list, not only the number.
- `lint · media files asked for`: the files the build asks for, by tier, and every non-explicit pool still at
  the default 4 (rule 8). Read it before any harvest.
- `lint · a look's format`: every non-explicit `_t3` look, each marked still or gif by its search words, listed
  in full. Read every line: a moving picture marked still is the miss (rule 6).
- `lint · a picture that misses its line`: a screen whose words are about her body (2+ body words) with no picture
  of a person or a body on it, and a scene named for a mirror, shower, window or bath whose picture of her never says
  it (rule 7). The media review page shows each picture's line beside it for the same reason.
- `lint · two people in her picture`: every `_t1`-`_t3` look spot whose description names a man and her, or any
  two people (a woman looking, a named person and her), in one frame (rule 9). "A waitress uniform" is her
  clothes, not a second person. An explicit spot is listed too when it shows one person watching the other
  ("staring", "in the doorway"). Two people having sex is the act itself, so it is not listed. Write the
  walk-in as what he sees: "Seen from a bathroom doorway: a naked young woman, 18, in the shower".
  Read it before any harvest; each name on it is rewritten as his view or kept because the touch is the picture.
- `one asset, one block` and `repeatable explicit media cycles`, as above.
- `--release`: "no missing media". Only then must the files exist.
