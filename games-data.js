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
    version: "0.1.6",
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
