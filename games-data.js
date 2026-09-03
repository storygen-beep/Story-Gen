// Single source of truth for the game portal.
// Both index.html (the grid) and game.html (the details page) render from this list.
// Add a game = add one entry here. Order = display order, newest first.
//
// Fields:
//   slug    (required) — folder under games/<slug>/, plays at games/<slug>/output/index.html
//   title   (required) — display name
//   summary (required) — one-paragraph player-facing teaser (the curated portal copy)
//   badge   (optional) — small tag shown next to the title, e.g. "New"
//   dev     (optional) — true → renders in the "Dev / test builds" section, "Open" affordance
//   version (optional) — the PUBLISHED release currently live at games/<slug>/output/, e.g. "0.1.3".
//                        Bump it in the same commit that rebuilds output/, and archive that build to
//                        games/<slug>/releases/v<version>.html. This is the number the storefronts
//                        (gamcore/mopoga/itch) ask for, so it must track what actually shipped —
//                        NOT whatever is currently half-built in the working tree.
window.GAMES = [
  {
    // Listed 2026-09-02. Authored with author-game-v2. 10 locations, 43 canvases, 5 characters,
    // 16 guidance cards, 5 walk-ins, 6,644 words, 43/44 gates.
    //
    // THE FIRST GAME IN THIS REPO WITH ARCS. Measured across twelve built games and 1,396
    // canvases, no character anywhere here had a second thing that happens — every hub and act
    // loop was authored in its converted state on day one. This one runs two numbered ladders:
    // Ray nine steps, Simone seven. The first third of each carries no sex at all; it buys when
    // the person is alone and what they are vulnerable about. The repeatable surface is what
    // finishing the ladder BUYS, not the starting position. references/the-arc.md A1-A12, and
    // v2_state.json records which of the twelve it built and which it skipped.
    //
    // Also first here: a parked refusal that ROUTES (saying no to Ray shortens Simone's step 3),
    // an aftermath beat on every act surface (23 of 23 finish nodes across six v2 games shipped
    // with an empty exit block), and block_pool, which is documented in four places and had been
    // used by zero v2 games.
    //
    // ⚠️ IT IS 15% WRITTEN AND THAT IS THE ONE RED GATE. 6,644 words against a declared 45,000.
    // The pledge house is the anchor and is supposed to hold 11,500; it holds 1,671, so the
    // KITCHEN is currently the de facto anchor at 31%. Every room works and every room is thin.
    // This is the same red night_desk carries and for the same reason — the skeleton is complete
    // and the flesh is not. 38,356 words owed, distributed per board.locations[].fill.
    //
    // ⚠️ THE PHONE WAS DECIDED, DESIGNED AND NEVER BUILT. sheets/SYSTEMS.md §7 specifies it —
    // messaging plus a feed she can post to, with the corruption_min finding and the hybrid that
    // works around it — and there is no 8_phone.toml and no [phone] block in the build. That is
    // exactly the mothers_place failure the-phone.md opens with, committed in the same session
    // that quoted it. Either build it or cut it from the systems sheet; it may not sit as a
    // declared system that does not exist.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 12 referenced files, ZERO on disk — 10 cycling pools
    // plus portraits and location plates. Run find-media, rebuild, add `version`, archive to
    // games/orientation/releases/, and drop `dev: true` in the same commit.
    //
    // ⚠️ THE EXPLICIT FLOOR IS A BARE PASS ON FIVE SCENES. 10.4% of repeatable beats, which
    // clears the floor only because the denominator is small. As the 38k gets written that ratio
    // falls unless the heat goes in WITH the fill rather than after it.
    //
    // ⚠️ THE TITLE HAS NOT BEEN CHECKED against the storefronts for a collision, and it is
    // immutable once anything ships.
    slug: "orientation",
    title: "Orientation",
    badge: "v2",
    dev: true,
    summary: `She is eighteen and she has been in this house four hours. Her mother married the man who owns it in June, his son is a junior at the college she starts tomorrow, and the room she has been given was an office until Sunday — the shelves are still on the wall. Tuition is his and he has never once said so out loud. Everything college charges on top of tuition is hers: the dues, the meal plan, the bus, and a hundred and twenty dollars every Friday counted on an office desk by a senior who decides who she is allowed to be on that campus and says so to her face. The house is on one side of a forty-minute bus route and the campus is on the other, and there are two ways across — pay, or ask a man. Her mother works nights, Sunday to Thursday, from ten. Everyone in that house knows what that means and nobody has said it.`,
  },
  {
    slug: "vesper",
    title: "Vesper",
    badge: "New",
    version: "0.2.0",
    summary: `An owned half-human weapon — the company's slave inside its tower, a false face outside — slips into powerful men's lives and drains them while they think they're using her, hunting a "rogue" who may be the one person who ever loved her. Phase 1: the cold open, her owner, and the wrecked boss she seduces and drains for the truth.`,
  },
  {
    slug: "media_lab",
    title: "Media Lab",
    dev: true,
    summary: `Not a game — a rig. One page, ten media slots, each probing a different way a media search fails: eye contact, withheld tease, flash-vs-strip, a load-bearing dark setting, an unshown finish, an affect gate, a people count, a position, a partner who must stay visible, and one SFW still. Round 2 of the find-media query study; three slots carry old-doctrine queries as a hidden control.`,
  },
];
