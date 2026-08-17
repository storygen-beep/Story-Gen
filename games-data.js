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
//   paidBuild (optional) — true → the details page also shows a button opening
//                        games/<slug>/output-paid/index.html, the supporter artifact built from the
//                        SAME merged TOML with `--build paid` (cheat-page rows live instead of
//                        padlocked). Only set it for games that author [ui.cheat_page]; rebuild BOTH
//                        outputs in the same commit or the two drift.
//   paidLabel (optional) — button text for that build; defaults to "🎯 Beta Nut Build".
//   version (optional) — the PUBLISHED release currently live at games/<slug>/output/, e.g. "0.1.3".
//                        Bump it in the same commit that rebuilds output/, and archive that build to
//                        games/<slug>/releases/v<version>.html. This is the number the storefronts
//                        (gamcore/mopoga/itch) ask for, so it must track what actually shipped —
//                        NOT whatever is currently half-built in the working tree.
window.GAMES = [
  {
    // Listed 2026-08-18. Authored end-to-end with author-game-v2, and the first game in this
    // repo to clear the scoreboard outright: 26/26 gates, 11,100 words across 9 locations,
    // 63 canvases, 5 characters, 29 guidance cards. Headless play-through is clean — no JS
    // errors, the opening funnel lands on the landing, and the seen-75 crossing renders greyed
    // from turn one.
    //
    // Premise came out of a measurement, not a mood. Of the mopoga top-30, exactly four run a
    // female protagonist, and every incest game in that thirty is male-POV — the daughter's side
    // exists only as a subsystem under somebody else's goal. All four fem-protag entries also run
    // ONE global corruption gate and all four generate stat-wall and cheat-code revolt, while the
    // only fem-capable entry running split ratcheting tiers has 6 grind complaints in 1,267. So:
    // that validated shape on four tiers, with the taboo as the spine rather than a side door.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 21 cycling pools plus the fixed slots, 9 location plates
    // and 5 portraits, with zero files on disk. Current output/ is a --dev --debug build, so the
    // art shows labelled debug placeholders rather than silent gaps and the dev stat controls are
    // visible. Run find-media, then rebuild output/ without --dev --debug, add `version`, archive
    // to games/the_allowance/releases/, and drop `dev: true` in the same commit.
    //
    // One open lint, logged in v2_state.json: 78% of choices open on turn one. The room-screen
    // texture legitimately opens on day one, but that is the number seventh_day failed on — judge
    // it in play before treating it as fine.
    slug: "the_allowance",
    title: "The Allowance",
    badge: "v2",
    dev: true,
    summary: `Nell Vasey was supposed to leave in September and the money was not there, so she is nineteen and still in the room she was eight in. Her father takes fifty a week in board off everyone in the house, counted at the kitchen table on a Sunday night and written down the back of an envelope in biro. Her Saturday job pays thirty-six. The gap is covered by an allowance she has to ask for out loud, itemised, in front of her mother and her brother and her uncle — so to pay her father she has to ask her father. One bathroom for five adults and a bolt that goes across an inch of air. A brother on nights whose window shares a flat roof with hers. An uncle in the box room that this family fills with whichever relative is between things. And a mother who works nights, sleeps eight until three with the door shut, and has now asked twice whether everything is alright in this house. Everything Nell climbs is a different way out from under one sum, and at the top of the last one the envelope runs the other way.`,
  },
  {
    // Listed 2026-08-17. Authored end-to-end with author-game-v2. 25,817 words across 14
    // locations, 149 canvases, 25/26 gates.
    //
    // The first game in this repo to ship all THREE content kinds the skill names: 25 standing
    // hubs, 14 TRIGGERED random events, and 7 milestones. That matters because its own v0.1 had
    // zero triggered content — every earlier game in this list has the same hole, and
    // the-release.md calls that layer the main heat engine for a female protagonist. Verified
    // live across 28 in-game days: events fire, replace the location page, and respect the
    // engine's 3-entry cooldown.
    //
    // The one red gate is `the climb is paid for`, and it is a CHECK bug, not a game defect —
    // gates.py counts the one-shot opening funnel as farmable 14 times. Satisfying it would mean
    // charging the player energy to read the intro. Written up as finding #5 in
    // games/seventh_day/ENGINE_NOTES.md, which carries six findings in total (two engine, four
    // skill), all unapplied and awaiting a call.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 52 cycling pools (246 clips), 8 fixed files, 14 location
    // plates and 6 portraits, with zero files on disk. Current output/ is a --dev --debug build,
    // so the art shows labelled debug placeholders rather than silent gaps, and the dev stat
    // controls are visible. Run find-media, then rebuild output/ without --dev --debug, add
    // `version`, archive to games/seventh_day/releases/, and drop `dev: true` in the same commit.
    slug: "seventh_day",
    title: "The Seventh Day",
    badge: "v2",
    dev: true,
    summary: `Fourteen people live on sixty acres at the end of a mile of gravel, under seven rules your father wrote out by hand and framed at the turn of the stair. Thea is the third daughter: no room of her own, no money that was ever hers, and a rota in her mother's handwriting that decides where her body is every hour of the week. The fourth rule specifies a garment. The sixth says no door is shut on two. The seventh says nothing is yours, and on the seventh day a tin comes round the bench to prove it. Everything she climbs is measured in reach, not rank — what she is allowed to be seen in, who she can be alone with and for how long, and which doors open for her without anybody being asked. Her brother walks the property every night at ten to make sure none of this happens.`,
  },
  {
    // Listed 2026-08-14. Authored end-to-end with author-game-v2 and the first game in this
    // repo to ship a PRODUCTION build on listing day: no --dev, no --debug, --build free, and
    // the archive at games/forty_miles/releases/v0.1.html is byte-identical to output/.
    // 37,450 words across 8 locations, 247 canvases, 20/20 gates, and an 11/11 headless
    // play-test (games/forty_miles/playtest.py) covering the money clamp, nine NPC presence
    // probes across the midnight and week boundaries, and the locked door staying locked.
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 84 declared slots — 68 cycling pools (296 clips),
    // 2 fixed files, 8 location plates, 6 portraits — with zero files on disk. Because this is
    // a non-debug build there are no labelled placeholders: the art simply is not there and the
    // page renders the prose with silent gaps. Run find-media, then rebuild output/ and
    // re-archive in the same commit. Flip `dev: true` if it should sit in the dev section
    // until then.
    slug: "forty_miles",
    title: "Forty Miles",
    badge: "v2",
    version: "0.1",
    summary: `Robyn Sayer works ten at night to six in the morning at a truckstop on a trunk road with nothing open either way for forty miles. At ten the day manager hands over and she is the site — the only authority on it, holding the only key to the shower block. At six she hands it back and is the girl on nights who owes the owner six thousand pounds he has never once explained. Everything she climbs buys hours, not rank: how much of the site is hers after dark, how much of her the lit glass box shows a road she cannot see into, and what she will sell that was never on the shelves. Nine cabs in the park, one man in the tyre bay who has nothing over her, and a padlocked door behind the cold store that is not the company's lock.`,
  },
  {
    // Listed 2026-08-12. First game authored end-to-end with the author-game-v2 skill:
    // 36,019 words across 8 locations, 18/18 gates, and a headless play-test (games/steam/playtest.py)
    // covering the money clamp, the schedule grid and the guidance ladders.
    // Current output/ is a --dev --debug build — dev stat controls visible, media NOT yet harvested,
    // so images and clips show debug placeholders. Add `version` + drop the dev flags on output/
    // when the production build ships with art.
    slug: "steam",
    title: "Steam",
    dev: true,
    summary: `Your aunt left you the Marlow Baths and the note on it: sixty-one thousand dollars, eleven months, and a hundred and thirty-five a week collected in person every Friday by the cousin who expected to inherit the building. You have one attendant who has not been paid since March, a boiler man who sleeps beside the boiler, and a spring that has run hot out of the mountain since 1891. The town knew your aunt as respectable. Keep the doors open and find out what the house used to do — and what it will pay you to do it again.`,
  },
  {
    slug: "vesper",
    title: "Vesper",
    badge: "New",
    version: "0.1.8",
    paidBuild: true,
    summary: `An owned half-human weapon — the company's slave inside its tower, a false face outside — slips into powerful men's lives and drains them while they think they're using her, hunting a "rogue" who may be the one person who ever loved her. Phase 1: the cold open, her owner, and the wrecked boss she seduces and drains for the truth.`,
  },
  {
    slug: "mothers_place",
    title: "Mother's Place",
    summary: `Cora, mid-twenties and broke, moves back into the house she grew up in a year after her mother walked out — and starts becoming the woman everyone's still waiting for.`,
  },
  {
    // Re-listed 2026-07-16 after the full re-author (v1 archived at archive/the_inheritance_v1/).
    // Current output/ is a --dev --debug build (dev stat controls visible, media not yet harvested);
    // add `version` + drop the dev flags on output/ when the production build + art ship.
    slug: "the_inheritance",
    title: "The Inheritance",
    badge: "New",
    summary: `Written out of the will and dragged home for the reading, you find your aunt already running your dead mother's failing hotel — and every relative certain you're nobody. Take the hotel in hand, and take every person under its roof, until the family that underestimated you answers to you.`,
  },
  {
    slug: "last_call",
    title: "Last Call",
    summary: `A woman in her mid-thirties inherits a failing bar and a debt she didn't sign for — weekly payments, romance, and survival.`,
  },
  {
    slug: "late_shifts",
    title: "Late Shifts",
    summary: `Maya, a 22-year-old linguistics dropout, returns home and works nights at a diner where she discovers power and corruption.`,
  },
  {
    slug: "under_one_roof",
    title: "Under One Roof",
    summary: `Lily Chen, 19, is stranded at her step-father's isolated rural property with his two adult sons — economics and desire under one roof.`,
  },
  {
    slug: "the_long_summer",
    title: "The Long Summer",
    summary: `Maya, eighteen, arrives at her stepfather's rural Alabama property and learns to navigate corruption, desire, and survival math.`,
  },
  {
    slug: "jacks_world",
    title: "Jack's World",
    summary: `Jack moves into his step-mom Angela's apartment, and over thirty days what started as practical becomes something neither expected.`,
  },
  {
    slug: "two_weeks",
    title: "Two Weeks",
    summary: `You return home for your step-brother's wedding with fourteen days to act on feelings you buried before he says "I do."`,
  },
  {
    slug: "new_in_town",
    title: "New In Town",
    summary: `Emma, a sheltered 23-year-old schoolteacher, moves to Millfield and awakens to power over four men through strategy and reputation.`,
  },
  {
    // Added 2026-08-11. The author-game-v2 skill's first game, and the first thing this project has
    // ever built that passes all ten gates (10/10, exit 0) — 36,035 words of location prose across
    // 8 locations, 97 canvases, 4 characters, 8 visible locked doors.
    // ⚠️ output/ is a --dev --debug build: dev stat controls in the sidebar, and 53 declared media
    // slots (49 pool_dir + 4 fixed) with ZERO files on disk, so every image/video renders as a
    // labelled placeholder. find-media has never run on it. Listed as dev until the media lands;
    // add `version` and drop the dev flags when a production build ships.
    slug: "back_home",
    title: "Back Home",
    badge: "v2",
    dev: true,
    summary: `June, 24, comes back on a coach with two bags after the job and the man both went — into her stepfather's house, where her room is half a storage room, the bathroom door does not lock, and her bedroom catch broke years ago because nobody ever needed it to. One bathroom and four adults; a lodger eighteen inches through the partition wall who is gone in the spring and replaced by somebody else. She was the one who got out. Now the men who were beneath her in that story have what she needs, and the house rearranges itself around what she wants without anybody ever saying the word for it. Built with author-game-v2: no ending, one house, and every release a rung on somebody already in it.`,
  },
  {
    slug: "the_long_summer_test",
    title: "The Long Summer — Test Slice",
    dev: true,
    summary: `A 10-day engine-validation slice with dev buttons visible.`,
  },
  {
    slug: "test_customize",
    title: "Coffee Shop Test",
    dev: true,
    summary: `A short test build for NPC name/relationship customization and variable syntax.`,
  },
  {
    slug: "media_lab_h",
    title: "Media Lab H",
    badge: "Shelved",
    dev: true,
    summary: `Ten unfilled media slots — a byte-identical copy of Media Lab F's beats (ten singles, no pool), built empty 2026-08-05 as the rig for the first DUMP-ALL find-media-v3 run. 30 queries stocked 1,932 options and installed nothing, so all ten slots read "N options — pick" and the game renders ten holes until they are picked by hand. Against Media Lab G's 195 options on the same beats, this is the measurement that the triage step was destroying the shelf. The run also killed the skill's "the browser cannot fan out" rule: three Chrome tabs harvested three slots at once, 6 round trips instead of 30.`,
  },
  {
    slug: "media_lab_g",
    title: "Media Lab G",
    dev: true,
    summary: `Ten unfilled media slots for the find-media query study — the clean rig for the first end-to-end find-media-v3 run. Nine single slots plus one pool (slot 8, target 4), so the run exercises the pool path that made vesper expensive. Beats copied from Media Lab F; TOML and build only, no media and no shelf, so every slot starts as "Not worked".`,
  },
  {
    slug: "media_lab_f",
    title: "Media Lab F",
    dev: true,
    summary: `Ten unfilled media slots for the find-media query study. Unfilled TOML-only testbed without copied media assets.`,
  },
  {
    slug: "media_lab_e",
    title: "Media Lab E",
    dev: true,
    summary: `Ten unfilled media slots for the find-media query study. Unfilled TOML-only testbed without copied media assets.`,
  },
  {
    slug: "media_lab_c",
    title: "Media Lab C",
    dev: true,
    summary: `Cloud-session replication of arm A: the same ten beats and the same candidate shelf as Media Lab, filled by the full find-media skill — gates, frame strip, and HEAT/SETTING/CRAFT ranking. Filled 2026-07-28, 10/10 slots, 16 min and 19 board reads; the strip rejected 55 of 98 candidates. Slot 6 came back POOL_GATE_UNSATISFIABLE, reproducing arm B independently. Write-up in games/media_lab_c/.find-media/FINDINGS.md.`,
  },
  {
    slug: "media_lab_d",
    title: "Media Lab D",
    badge: "Filled",
    dev: true,
    summary: `Cloud-session replication of arm B, run 2026-07-28: all ten slots filled by find-media-b — correctness gates plus the frame strip, installing the first clip that passes, no ranking. 10/10 installed in 17m09s from 32 image reads, 54 candidates examined, 44 gate rejects. Two installs are gate-correct and visibly rough (a 3-panel collage, a watermarked stock still) and the facial slot found nothing correct in 24 candidates — exactly the cost of deleting the ranking step. Numbers in games/media_lab_d/RUN_RESULT.md.`,
  },
  {
    slug: "media_lab_b",
    title: "Media Lab B",
    dev: true,
    summary: `Arm B of the ranking experiment. The same ten beats and the same candidate shelf as Media Lab, filled by the find-media-b skill: correctness checks only — gates plus the frame strip — then it installs the FIRST clip that passes. No heat scoring, no ranking, no taste. Compare its picks against Media Lab's to see whether the ranking step earns its keep.`,
  },
  {
    slug: "media_lab",
    title: "Media Lab",
    dev: true,
    summary: `Not a game — a rig. One page, ten media slots, each probing a different way a media search fails: eye contact, withheld tease, flash-vs-strip, a load-bearing dark setting, an unshown finish, an affect gate, a people count, a position, a partner who must stay visible, and one SFW still. Round 2 of the find-media query study; three slots carry old-doctrine queries as a hidden control.`,
  },
];
