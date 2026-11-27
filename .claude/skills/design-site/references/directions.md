# Step 3 method — three directions that are real choices

A direction is a point of view about how this business should look, written down fully enough to build
from. Three palette swaps of the same page are one direction shown three times.

## Where a direction comes from

Work in this order. The style library comes last on purpose.

1. **The brief.** Write three to five attributes the brand should carry, as plain adjectives the
   audience would use ("unhurried", "exacting", "neighbourly"). Every later choice must trace to one.
2. **A world outside websites.** For each direction pick one non-web source that already carries those
   attributes — packaging, signage, a printed form, a map, a magazine, an instrument panel, a shopfront,
   a material. Use the "Non-UI sources" table in
   [vendor/inspiration-sources.md](vendor/inspiration-sources.md). Take **one** concrete thing from it
   and record it in that file's `Taken / Not taken / Serves` form. One thing taken, not the whole look.
   Work from what you know of these sources; do not fetch galleries or other companies' sites.
3. **Typeface by reasoning.** Go from attribute to construction to candidate with the table in
   [vendor/typography.md](vendor/typography.md). Fonts on its watch list need a written reason. Faces
   must be on Google Fonts (the only font host an Artifact can load) or be a system stack from
   [tokens/system-font-stacks.md](tokens/system-font-stacks.md).
4. **Colour generated, not picked.** Follow `.claude/skills/better-colors/SKILL.md`: one neutral ramp,
   one accent ramp, each step with a job. Start the neutral from a tinted scale in
   [tokens/radix-neutrals.json](tokens/radix-neutrals.json) that leans toward the accent; derive the
   accent hue from the direction's source world, not from a palette list.
5. **The style library, as a mood.** `.claude/skills/awesome-design-skills/` and the
   `ui-ux-pro-max` search may suggest a layout feel, density or mood. Never lift their fonts or hex
   values unchanged: many of those are the overused defaults this step exists to avoid.

## The three slots

| slot | what it is |
|---|---|
| **Familiar** | What the category's best sites look like structurally, executed with care. Lowest risk. |
| **From the brief** | Derived only from steps 1–4 above. Do not open the style library for this one. |
| **Bolder** | A clear step further in type or colour, still appropriate for the audience. |

If the user named a style, it replaces the Familiar or Bolder slot. The From-the-brief slot always stays.

## Write each direction down

One `DESIGN.md` per direction at `<work>/directions/<a|b|c>/DESIGN.md`, in the format in
[vendor/design-md-spec.md](vendor/design-md-spec.md):

- Front matter: `name`, `description`, `colors` (include `primary`, `neutral`, `surface`, an accent as
  `tertiary`, and an `on-…` colour for text on each fill), `typography` (display, headings, body,
  label), `rounded`, `spacing`, and `components` for at least `button-primary` (with hover) and the
  form input.
- Sections: Overview (the attributes and the source world, with its Taken / Not taken line), Colors,
  Typography, Layout, Shapes, Components, Do's and Don'ts.
- Sizes from `scripts/scale.py type` and `scale.py space`; motion timing, if any, from
  [tokens/open-props-easing.css](tokens/open-props-easing.css).

## Gate — nothing reaches the user until all three pass

```bash
npx -y -p @google/design.md designmd lint <work>/directions/a/DESIGN.md     # each of the three
python3 .claude/skills/design-site/scripts/directions.py <work>/directions/{a,b,c}/DESIGN.md --previous 'sites/*/design-brief.json'
python3 .claude/skills/design-site/scripts/build.py preview <work>/options.html <work>/options-preview
.claude/skills/impeccable/scripts/impeccable detect <work>/options-preview/index.html
node .claude/skills/design-site/scripts/check.cjs '<work>/options-preview/index.html#b' <work>/options-shots/b   # and #a, #c
```

- `designmd lint`: no errors. Contrast warnings are errors here. An "orphaned token" warning is fine.
- `directions.py`: `ok: true`. A flagged tell is fixed, or kept only with a reason written in the
  direction's Overview and repeated to the user ("uses Inter because …").
- `impeccable detect`: no findings, same exception rule.
- Look at each direction's phone and desktop fold screenshot once. Fix what is broken.

If the linter or detector cannot run, say so when presenting the options — never present a direction
as checked when it was not.

## After the user picks

Copy the chosen `DESIGN.md` to `<work>/DESIGN.md`. It is the build spec for step 4 and the standard
reviewers judge against in step 5. A mix ("fonts from A, colours from C") is written as a new
`DESIGN.md` and put through the same gate before building.
