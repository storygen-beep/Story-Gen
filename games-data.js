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
window.GAMES = [
  {
    slug: "vesper",
    title: "Vesper",
    badge: "New",
    summary: `An owned half-human weapon — the company's slave inside its tower, a false face outside — slips into powerful men's lives and drains them while they think they're using her, hunting a "rogue" who may be the one person who ever loved her. Phase 1: the cold open, her owner, and the wrecked boss she seduces and drains for the truth.`,
  },
  {
    slug: "mothers_place",
    title: "Mother's Place",
    summary: `Cora, mid-twenties and broke, moves back into the house she grew up in a year after her mother walked out — and starts becoming the woman everyone's still waiting for.`,
  },
  {
    slug: "the_inheritance",
    title: "The Inheritance",
    summary: `Catherine returns home for a will reading, seducing family and outsiders to claim the estate and break her stepmother's control.`,
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
];
