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
    slug: "vesper",
    title: "Vesper",
    badge: "New",
    version: "0.1.5",
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
