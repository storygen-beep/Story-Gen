# Media blocks — which screens get one, and where it goes

A media block is the picture or clip spot on a screen: a `type = "image"` or `type = "video"` block whose `props`
carry `description`, `search_queries`, and either `pool_dir` (a folder the engine cycles, one file a visit) or `file`.
The author writes the block when the scene is written. The file itself comes later, at "release ready?": an empty
pool renders nothing and goes on the missing-media page (`generators/v2.py`, `missing_media.append` in the pool
renderer). So a block costs nothing to write early, and a scene written without one is a scene that will ship
without a picture.

Taught from first_term's release 1 pass (LO, 2026-11-12: "We have not been mentioning the media blocks at all"),
where 24 of 167 shipped screens had media and the everyday screens had none.

## What gets a block

| the screen | the block |
|---|---|
| a body moment: a look, something shows, sex, her own hand | a clip (or still) right after the line that says it, on the same screen |
| a screen she sees often (class, shift, dinner, bed, the park) | one rotating pool, first on the screen |
| a person's hub (his room, her kitchen) | one rotating picture of that person, first on the screen |
| a one-time step | one picture or clip on its key line |
| a talk screen at a hub (each choice opens one) | one picture of that person doing what the screen says; the hub's own picture is gone once the choice opens the new screen |
| a door, a notice, a system screen | none, written down as none with the reason |

## Every screen, not every scene
Count by screen. A scene with a picture on its first screen still leaves every other screen bare, and each choice
opens a new screen: the picture before it is gone. Taught from first_term (LO, 2026-11-12: "Mark in living room also
didn't have media for all interaction with him… I think there could be a lot more similar scenes"), where two passes
counted a scene as done once any of its screens had a block, and 320 of release 1's 448 screens had none.

A canvas written by hand in a phase file, not by the build scripts, takes its blocks in that file. A build that
places blocks from a table must stop when a row never lands, or the row is lost without a word.

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
   - `_t0` everyday, a still
   - `_t3` a look, a towel, cleavage, a still
   - `_t4` skin, a still or a clip
   - `_t5` sex or masturbation, animated only
   - `sex/` for `_t4`/`_t5`; the gates count `_t4`, `_t5` and `sex/` as explicit
7. **Describe it for the search, and read it as an adult.** `description` says what the frame shows, with the
   people's ages when they matter (every person is an adult). `search_queries` are two or three plain search
   phrases. No gate reads either one. The media review does.
8. **No harvest while writing.** Writing a block never means searching or downloading. The files come when the
   person who owns the game asks for them.

## How it is checked
- `lint · a screen without media`: every screen with no block of its own, listed (a door is rightly none, so it
  never fails). Read the list each release; each name on it has a block or a reason on the media sheet.
- `an explicit beat carries a clip`: at least 50% of explicit beats carry their own clip. Its report lists every
  screen still missing one, so read the list, not only the number.
- `one asset, one block` and `repeatable explicit media cycles`, as above.
- `--release`: "no missing media". Only then must the files exist.
