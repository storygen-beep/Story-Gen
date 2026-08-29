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
    // Listed 2026-08-30. Authored end-to-end with author-game-v2. 8,202 words across 10
    // locations, 52 canvases, 5 characters, 10 guidance cards, 46/46 gates with ZERO n/a —
    // the first game here where no check reported an absence.
    //
    // Built against the shape the previous eight kept landing on. SIX of the eight v2 games are
    // a female protagonist and blood family, so the premise was never going to differentiate
    // this one — the corpus says premise is 0 of 30 reasons a game in this genre is loved, and
    // freedom is the largest at 25.9%. So the differentiation went into the three §1
    // declarations every earlier game answered by default: `written` recorded as a CHOICE, a
    // start choice shipped in 0.1 rather than retrofitted (the intake form asks what she did
    // before, three answers, each read at five sites), and `relationship_options` on two of the
    // men — the player names what her brother and the last client are to her, and the prose
    // reads it back through @dane.rel and @marlon.rel.
    //
    // The structural move is that she has a JOB that makes her visit people. A home health aide
    // route forces the map to be a town rather than one household, makes the repeatable surface
    // body contact by construction (the bath chair, the bed change), and answers release 41
    // mechanically: a new house on the sheet.
    //
    // `who_climbs = "cast"` with `ascent_tiers` EMPTY — 100% of the climb sits on the cast, and
    // the meter that widens the map belongs to a person: Cheryl's `trust` is the route. There is
    // no player ascent tier in this game at all.
    //
    // Firsts for this repo: 87 `block_pool` uses, the most of any game here; the wardrobe read as
    // a COLOUR rather than a lock (five variant selectors, no refusals); and five talk screens,
    // the genre's second-largest content kind, which no v2 game had built.
    //
    // ⚠️ FOUR DEFECTS THE 46 SOURCE GATES COULD NOT SEE, all found by the build and the live run:
    // `targetType = "canvas"` is not a valid choice target (importer takes trigger|location|node
    // — both act loops were unreachable); `exit_block.type = "choice"` is invalid; `outfit` is
    // not one of the seven VALID_CLOTHING_SLOTS; and `npc` is a TRIGGER field, so ten hubs
    // carried it at canvas level and rendered no portrait while the gate reported n/a, not FAIL.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 35 files missing at build time. Current output/ is a
    // --dev --debug build, so the art shows labelled debug placeholders rather than silent gaps.
    // Run find-media, rebuild WITHOUT --dev --debug, add `version`, archive to
    // games/the_route/releases/, and drop `dev: true` in the same commit.
    //
    // ⚠️ Open debts, all logged in v2_state.json promises: Marlon tops out at want 20 with no act
    // loop of his own; every dispatch host produces ONE outcome where the doctrine wants three;
    // no phone (P1's three questions pass on paper, revisit at 0.3); and `board.map.r1_signoff`
    // is still null — the map has not been signed off by anyone but its author.
    slug: "the_route",
    title: "The Route",
    badge: "v2",
    dev: true,
    summary: `Nora Ashby is twenty-seven and drives a county home care route: six houses off a two-lane road, get people up, get them washed, get them through the day, forty-five minutes a card. Two of the six are hers. Her father since the stroke in March, who ran everything and decided everything and now cannot get a sock on without her. Her brother since the wreck, home on a rebuilt knee with nothing to do all day but listen for her truck. Her uncle holds the power of attorney, which means the man who signs her timesheet is deciding how long she spends alone in that house — and he has never once said what he thinks that is worth. Above all of it is the woman at the agency who assigns the route, reads the hours back to her every Friday, and is the only person in the county who can take any of it away. Rent is Monday. The tank is half full. Nobody has ever had to explain why she is the one in the room.`,
  },
  {
    // Listed 2026-08-25. Authored end-to-end with author-game-v2. 10,297 words across 14
    // locations, 91 canvases, 6 characters, 14 guidance cards, 41/41 gates — the first game
    // here to take the whole scoreboard.
    //
    // Built to miss the shape the earlier seven kept landing on. FIVE of the seven v2 games are
    // a female protagonist and incest in a household she was already inside — daughter returns
    // (back_home), daughter never left (the_allowance), mother and son (off_season), cult
    // household (seventh_day), picking crew (the_season). This one marries her IN: eleven weeks
    // a Vance, a prenup that gives her nothing for three years, and a husband who hauls four
    // nights out of seven. The title is real and everything under it belongs to his sons. Nobody
    // in the repo has been an in-law before.
    //
    // `who_climbs = "cast"`, declared before a meter was named: 100% of the climb sits on the
    // cast. ONE willingness word (`want`) on all six at the same scale, per W6 as rewritten
    // 2026-08-24 — nine of thirteen field games do exactly that, and off_season's four
    // vocabularies for four people were the old reading. The rich second meter (`trust`) is on
    // Cade and Booth only, the two arcs that carry the game.
    //
    // Firsts for this repo: `block_pool` used in a v2 game at all (46 pools — every v2 game
    // before this shipped ZERO against the_long_summer's 46); every act surface built as a
    // node-routed loop rather than a one-shot cascade; a second `[[npcs.schedules]]` row split
    // out of every day-specific overnight window, live-probed at Saturday 01:00.
    //
    // Headless play-through is clean. Zero JS errors across the opening, all 14 locations, the
    // eleven hubs and all six act loops. The funnel hands over at Monday 07:05 into an office
    // with Cade standing in it, and the presence grid was probed at eight points across the week.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 29 cycling pools plus the fixed plates and portraits,
    // zero files on disk. Current output/ is a --dev --debug build, so the art shows labelled
    // debug placeholders rather than silent gaps. Run find-media, rebuild output/ WITHOUT
    // --dev --debug, add `version`, archive to games/mrs_vance/releases/, and drop `dev: true`
    // in the same commit.
    //
    // ⚠️ Open debts, all logged in v2_state.json promises: Dorn carries `want` and gates NOTHING
    // (he is the week's clock, not a ladder, and that is deliberate for 0.1); nine locations have
    // no first-visit canvas, though the anchor does; three dispatch hosts produce ONE outcome
    // each; and the world ships 10,297 words against a 16,000-word finished plan kept per
    // location as `fill_finished` — every release until that closes adds words to existing rooms
    // rather than rooms.
    slug: "mrs_vance",
    title: "Mrs. Vance",
    badge: "v2",
    dev: true,
    summary: `Rilla Vance is twenty-seven and eleven weeks married to the man who owns Vance Diesel — four bays and a wrecker on a county road, with the house out back on the same gravel. She signed a paper before the wedding that says nothing here is hers for three years: no car in her name, not on the account, an envelope on the kitchen counter once a week. What he did give her is the book. She writes down every number the yard makes and cannot spend one of them, and every Friday his eldest son counts the cash drawer against her handwriting. Dorn hauls four nights out of seven. So the man whose authority she is borrowing is gone most of the week, and the four men the paper says she is over are all still here — the one who runs the yard and is two years older than his stepmother, the one who watches and never speaks, the nineteen-year-old who says the title like he means it, and the brother-in-law over the office who knew about the wedding before she did. Her own brother works the parts wall, because she got him the job.`,
  },
  {
    // Listed 2026-08-23. Authored end-to-end with author-game-v2. 4,411 words across 8
    // locations, 35 canvases, 5 characters, 13 guidance cards, 38/39 gates.
    //
    // Built against the shape the previous five kept returning to. FOUR of the six earlier v2
    // games are a female protagonist and incest inside ONE BUILDING with vertical authority
    // (back_home, the_allowance, off_season, seventh_day), which is the failure the-map.md R0
    // names in its own text. This one roots the map OUTDOORS on a packing yard — the world
    // contains the camp rather than the other way round — and puts the whole cast on a migrant
    // picking crew, so the taboo is proximity rather than a household. `who_climbs = "both"`,
    // declared: 57% of the climb sits on the cast, and five characters carry FOUR distinct meter
    // shapes where all five earlier games shipped one.
    //
    // First game here to clear `every hub is met first` — all six earlier v2 games ship the
    // forbidden cold-spawn hub, where a repeatable canvas with npc= IS the introduction. Also
    // the first with rungs at the FIELD's spacing (lowest at 4 and 5) rather than the DoL seed's
    // 15, which every one of the sixteen tiers across five games had copied.
    //
    // Headless play-through is clean: zero JS errors across the opening, the yard, the hubs and
    // both act loops; the day-cap fires and R7's free door keeps the spent screen alive.
    //
    // ⚠️ ONE RED GATE, and it is a real debt: `location fill`. 4,411 words against a 15,500-word
    // budget declared before the prose — 28%. The estimate was mine and it was ~3.5x optimistic.
    // At 102 words/canvas the writing is DENSER than the DoL seed (~68/unit); what the world is
    // short of is SURFACE COUNT — 35 canvases across 8 locations against the seed's ~68 units per
    // location. Deliberately NOT edited down to match, because a budget quietly revised to the
    // delivered count is the back-fill defect state.md exists to stop. Same posture as off_season.
    //
    // ⚠️ Also open: the anchor AS BUILT is the_camp (25%), not the declared the_packing_shed —
    // content gravitated to Wade's loop while the shed's own arc (Boyd's) is deferred to 0.2.
    // Resolve by filling the shed, not by moving the label. And npc_halbrook + the_porch were
    // cut to 0.2 as a whole unit before the writing, logged in WANT.md's amendments.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 27 declared slots — cycling pools on 6 of 8 locations
    // plus the fixed plates and portraits — with zero files on disk. Current output/ is a
    // --dev --debug build, so the art shows labelled debug placeholders rather than silent gaps
    // and the dev stat controls are visible. Run find-media, then rebuild output/ without
    // --dev --debug, add `version`, archive to games/the_season/releases/, and drop `dev: true`
    // in the same commit.
    slug: "the_season",
    title: "The Season",
    badge: "v2",
    dev: true,
    summary: `Cass Renfro has picked six seasons and has never once held her own money. The crew is her father, her two brothers, her uncle and four men who are not family, and they follow the fruit — nine weeks at this farm, then the next one, living out of two vans and a camp trailer parked on the packing yard. Everyone is paid by the bin and every bin goes through the man whose name is on the contract, which has never been hers. She gets the back bunk because she is the only woman on the crew and because her father says she does. There is no door on this property that locks except the cooler, the shower gate starts at her knees and stops at her collarbone, and the wall between her bunk and her brothers is one sheet of plywood. Nothing here is private and nobody is further away than the yard, which is the whole problem and the entire appeal.`,
  },
  {
    // Listed 2026-08-19. Authored end-to-end with author-game-v2. 7,963 words across 10
    // locations, 58 canvases, 4 characters, 14 guidance cards, 31/32 gates.
    //
    // Built to break a skeleton, not for novelty. Three of the five earlier v2 games
    // (back_home, the_allowance, seventh_day) are the SAME shape — a young woman at the bottom
    // of a household, world = interior, family men above her — and the-map.md R0 says so in its
    // own text. This inverts all three axes the skill demands be declared and all five left on
    // default: she is the ELDER (mother/sister/aunt), the map is `street_mesh` with the exterior
    // as the root, and `who_climbs = "cast"` measures at 100% of the climb on the cast against a
    // previous 19-29% — a band no shipped game in the 25-game corpus occupies. Four characters,
    // FOUR DISTINCT meter shapes, where all five earlier games shipped one.
    //
    // Also the first here to ship the two things v2 has never shipped: a node-routed act menu
    // (Tam's pose ladder, with the locked door inside it) and the talk screen at 4 conversations
    // deep. Explicit floor 14.8% against a 7.5% floor, reached by rewriting 36 beats that were
    // scoring 1-2 — register.md's pivot signature — with no gratuitous nouns added.
    //
    // ⚠️ ONE RED GATE, and it is a real debt, not a check bug: `location fill`. The board declared
    // 33,300 words before the prose, in round numbers, and 7,963 shipped — 24%. The budget was a
    // real plan and it was wrong in the over-declaring direction. It has deliberately NOT been
    // edited down to match, because a budget quietly revised to the delivered count is the
    // back-fill defect state.md exists to stop. Open call in games/off_season/v2_state.json:
    // write the remaining ~25,400 words, or re-budget deliberately and log the amendment.
    //
    // ⚠️ MEDIA HAS NEVER BEEN HARVESTED. 32 cycling pools (151 clips) plus 12 fixed slots, 10
    // location plates and 4 portraits, zero files on disk. Current output/ is a --dev --debug
    // build, so the art shows labelled debug placeholders rather than silent gaps and the dev
    // stat controls are visible. Run find-media, then rebuild output/ without --dev --debug, add
    // `version`, archive to games/off_season/releases/, and drop `dev: true` in the same commit.
    slug: "off_season",
    title: "Off Season",
    badge: "v2",
    dev: true,
    summary: `Marnie Kesh has her own name in eight-foot letters over the front of a seaside arcade that nobody walks past between October and April. Her husband has been inside four years for what he did in its back room with its money. She lives in the flat above it, feeds three pounds at a time into a coin meter to make the place warm enough to take her coat off in, and every Monday ninety pounds of pitch rent leaves her hand — into her eldest son's, because he holds the lease and took the books off her the month his father went away. Her two sons, her younger brother and her sister's girl all live inside four hundred yards of that counter, and none of them under her roof. She raised or reared every one of them and there is nothing left in this town that needs her to. Everything she climbs is somebody coming to her instead of her going to them, and it climbs on four separate ladders, because in this one the cast is what changes and not her.`,
  },
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
    version: "0.2.0",
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
