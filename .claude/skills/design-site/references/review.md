# Step 5 reviewer briefs

Three reviewers, launched in one message so they run in parallel (Agent tool, `general-purpose`).
Each is read-only: it reports, it does not edit. Give each reviewer the paths below and its brief, and
nothing about what you think of the page — a reviewer handed a conclusion returns it confirmed.

Fill in before sending:

- `<work>` — the site's working folder
- `<page>` — `<work>/page.html` (the source) and `<work>/preview/index.html` (rendered form)
- `<shots>` — `<work>/shots/{phone,tablet,desktop}-{fold,full}.png`
- `<brief>` — `<work>/brief.json`

Every reviewer returns findings in this exact shape, most important first, at most ten:

```
[severity: blocker|major|minor] <what is wrong, in one sentence a non-designer understands>
  where: <section or selector>
  evidence: <what you saw or measured>
  fix: <the specific change>
```

and ends with one line: `Strongest thing about this page: ...` so the merge keeps what works.

---

## Reviewer A — design quality

> You are reviewing a web page's visual design. Read `.claude/skills/impeccable/reference/critique-rubric.md`
> and the "AI-generated tells" list in `.claude/skills/design-site/references/conversion-rules.md`.
> Then look at the screenshots at `<shots>` (read the image files — fold and full, phone and desktop),
> the source at `<page>`, the detector output at `<work>/detect.txt`, and the design sheet at
> `<work>/DESIGN.md` — the page is supposed to follow it, so report every place it does not (a colour,
> size, radius or font that is not in the sheet).
>
> Judge: visual hierarchy (is the most important thing the most prominent), typography (scale, line
> length, pairing), spacing rhythm, colour and contrast, consistency of repeated elements, whether the
> page looks like its chosen direction, whether it looks generated, and how it holds up on the phone
> screenshot. Do not comment on copy or conversion; another reviewer has those.
>
> Report findings in the required shape. Do not edit any file.

## Reviewer B — conversion

> You are reviewing a web page for how well it will convert visitors. Read
> `.claude/skills/cro/SKILL.md` and `.claude/skills/design-site/references/conversion-rules.md`.
> Then read `<brief>` (the goal, audience, traffic source and offer), the source at `<page>`, the
> measurements at `<work>/check.json`, and look at `<shots>` phone-fold and desktop-fold.
>
> Work through the cro skill's analysis framework in its stated order. Check specifically: can a
> stranger say what is sold from the first screen alone; does the headline match the traffic source in
> the brief; is there one primary action, visible without scrolling on the phone; is proof present,
> specific and near the top; are objections answered; is price clear; is the form as short as it can
> be. Flag any invented-looking proof and any `data-placeholder` still on the page.
>
> Where the evidence for a recommendation is weak (button wording, pricing layout), say so and mark it
> as something to test rather than a defect.
>
> Report findings in the required shape. Do not edit any file.

## Reviewer C — usability and accessibility

> You are reviewing a web page for usability and accessibility. Read
> `.claude/skills/web-design-guidelines/references/command.md` and apply its rules to `<page>`.
> Then read the automated scan at `<work>/a11y.json` (if the file is missing, say the scan did not run)
> and the measurements at `<work>/check.json` — in particular `targetsUnder24px`, `imagesMissingAlt`,
> `fieldsMissingAutocomplete`, `horizontalOverflowPx`, `consoleErrors`.
>
> Also check by reading the source: heading order, landmark elements, labels on every control, visible
> focus styles, `prefers-reduced-motion` handling, link and button semantics, form error handling.
> Translate each scan violation into plain language; group repeats of the same rule into one finding.
>
> Report findings in the required shape. Do not edit any file.

---

## Merging

1. Same problem reported twice → keep the clearer one, note both reviewers found it.
2. Reviewers disagree (A wants it bolder, B wants it calmer) → present it as a choice for the user, with
   your recommendation, not as a finding.
3. Anything that reverses a decision recorded in `brief.json` → drop it, unless it is a blocker, in which
   case say plainly that it conflicts with an earlier choice.
4. Rank: conversion blockers, accessibility blockers, majors (any reviewer), minors.
5. Show the user at most twelve findings. Count the rest in one line.
