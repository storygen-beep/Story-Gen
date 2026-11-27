---
name: design-site
description: Guided, step-by-step website design in one command. Interviews the user, proposes copy and three rendered visual directions, builds the page as an Artifact, reviews it for design quality, conversion and accessibility, and exports a site folder plus zip only when the user says it is ready. Use when the user runs /design-site, or asks to "design a website / landing page for me", "help me design a site step by step", "give me design options for my site", or to resume or export a site started with this command.
argument-hint: "[site name or one-line description] [fast] | resume <slug> | export <slug>"
---

# design-site — one command, seven stops

You are running a design studio's process for one client, the user. They are not a designer. Each step
you do the work, show something they can look at, recommend one option, and ask. You never make them
choose from descriptions when you could show them the thing.

Read these before step 1; they are short and the whole flow depends on them:

- [references/conversion-rules.md](references/conversion-rules.md) — the evidence-backed rules every page is built and reviewed against
- [references/artifact-rules.md](references/artifact-rules.md) — what an Artifact page can and cannot contain
- [references/review.md](references/review.md) — the three reviewer briefs used in step 5

## Ground rules

1. **Artifacts first, repo last.** All work happens in Artifacts and in the working folder below.
   Nothing is written to the repository until step 7's export, and only if the user says to export.
2. **Every step ends with a question** asked through `AskUserQuestion`: 2–4 concrete options, your
   recommendation first and labelled "(Recommended)", each with a one-line reason. The user can always
   type their own answer. Never ask a question you could answer from the brief.
3. **Show, then ask.** Publish or update the Artifact (or write the short text proposal) *before* the
   question, and say in one line what to look at. The question dialog may hide earlier text, so each
   question must make sense on its own.
4. **One role per skill.** The installed design skills disagree with each other. `frontend-design`
   builds. Everything else supplies material or reviews. Do not load a second builder mid-page.
5. **No invented proof.** Never fabricate testimonials, customer logos, review counts, statistics or
   press mentions. Where proof is missing, build a clearly marked placeholder (`data-placeholder`) and
   list it in the brief's `needs_from_user`. A page with invented proof is not shippable.
6. **Fast mode.** If the user passed `fast` or says "you decide", take your own recommendation at each
   step, say what you chose in one line, and stop only at steps 3 and 4 (the look and the built page)
   and before export.
7. **Save state after every step.** A resumed session reads the brief and carries on from `step`.

## Working folder and state

`<scratchpad>/design-site/<slug>/` (the session scratchpad; `<slug>` is a short kebab-case site name):

| file | what it is |
|---|---|
| `brief.json` | the state: every answer and decision, plus `step` |
| `options.html` | Artifact 1 — the three visual directions |
| `page.html` | Artifact 2 — the page itself (the single source of truth for the design) |
| `preview/`, `shots/` | local render and screenshots for review |

`brief.json` shape (add keys as needed, never rename these):

```json
{
  "slug": "", "step": 1, "fast": false,
  "business": {"what": "", "audience": "", "problem": "", "differentiator": ""},
  "page": {"type": "landing", "goal": "", "traffic": "", "offer": "", "price_shown": true},
  "proof": {"have": [], "needs_from_user": []},
  "message": {"headline": "", "subhead": "", "primary_cta": "", "sections": [], "meta_description": ""},
  "look": {"chosen": "", "tokens": {}, "fonts": [], "notes": ""},
  "artifacts": {"options_url": "", "page_url": ""},
  "review": {"applied": [], "declined": []},
  "motion": "none",
  "decisions": []
}
```

Append a one-line entry to `decisions` at every step (what was chosen and why). On `resume <slug>`,
read the brief, tell the user in two lines where things stand, and continue. If the scratchpad copy
is gone but `sites/<slug>/design-brief.json` exists, resume from that.

Scripts (run with absolute paths; they print JSON):

```bash
python3 .claude/skills/design-site/scripts/build.py preview <page.html> <out_dir>      # wrap the fragment for local rendering
node    .claude/skills/design-site/scripts/check.cjs <out_dir>/index.html <shots_dir>  # screenshots + measurements
python3 .claude/skills/design-site/scripts/build.py export <page.html> sites/<slug> <brief.json>
```

---

## Step 1 — Brief

Goal: know what is being sold, to whom, and the one thing the page must get a visitor to do.

1. If the user gave no description, ask in plain chat for two or three sentences: what they sell, who
   buys it, and what they want visitors to do. If they shared a URL or files, read those first.
2. Draft the whole brief yourself from what you have. Guess sensibly and mark guesses.
3. Ask (one `AskUserQuestion` call, up to four questions) only what you could not infer. Typical:
   the single conversion goal; where traffic will come from (ads, search, social, direct); what proof
   exists (reviews, logos, numbers, guarantees, none yet); whether price is shown on the page.
4. Show the brief back as a short list and ask: **approve / change something**.

The traffic source matters more than it sounds: the headline has to match what the visitor just
clicked (conversion rule 7). If traffic is paid ads, ask for the ad's promise or keyword.

## Step 2 — Message

Goal: the words and the order of the page, before any visuals.

1. Read `.claude/skills/copywriting/SKILL.md` and follow its "blank brief" path. For a pricing section
   also read `.claude/skills/pricing/SKILL.md`; for a signup form, `.claude/skills/signup/SKILL.md`.
2. Write three headline directions that differ in *angle*, not wording — for example outcome-led,
   problem-led, proof-led — each with its subhead and primary button label.
3. Propose the section order from the page anatomy in `references/conversion-rules.md`, cut to what
   this brief can actually fill. Fewer real sections beat more padded ones.
4. Show headlines and outline in chat, then ask: **which headline** (recommend one, say why in terms
   of the traffic source) and **approve the outline / change it**.

Copy rules: plain words, about a 6th-grade reading level, short sentences; the button says what
happens next; one goal per page.

## Step 3 — Look

Goal: the user picks a visual direction by looking at three real ones.

1. Gather raw material — three directions that are genuinely different in character, each a fit for
   this audience:
   - `.claude/skills/awesome-design-skills/SKILL.md` index, then the chosen styles' `SKILL.md` + `DESIGN.md`
   - `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <keywords>" --design-system`
     for palettes and font pairs (treat as suggestions, not law)
   - `.claude/skills/frontend-design/SKILL.md` — its list of AI-default looks. None of the three
     directions may be one of those defaults unless the user asked for it.
   One direction should be the safe, category-familiar choice; one a clear step bolder; one in between
   or a different mood entirely. Familiar structure, distinctive craft (see "first impressions" in the
   conversion rules).
2. Load the `artifact-design` skill, then write `options.html`: one page, three tabs, each tab the
   **hero plus the next section** using the approved headline, subhead and button — not lorem ipsum.
   Scope each direction under its own wrapper class with its own tokens. Give each a short name and one
   sentence on who it suits. See `references/artifact-rules.md` for the tab pattern.
3. Publish it (`Artifact`, `icon: "palette"`), save the URL to the brief.
4. Ask: **which direction** (recommend one, with the reason tied to the audience), with an explicit
   option to mix ("fonts from A, colours from C") or to see three new ones.

If the user asks for new options, replace the rejected ones and republish to the same Artifact.

## Step 4 — Build

Goal: the full page, as Artifact 2.

1. Read `.claude/skills/frontend-design/SKILL.md` in full and follow its two-pass process, with the
   chosen direction's tokens and the approved copy as the brief. It is the only builder.
2. Write `page.html` following `references/artifact-rules.md` and every build-time rule in
   `references/conversion-rules.md`. Mark the main action button(s) `data-cta="primary"` — the checker
   and the reviewers rely on it.
3. Render and look before publishing:
   `build.py preview` → `check.cjs` → read `phone-fold.png` and `desktop-fold.png`. Fix anything
   broken (overflow, a font that failed to load, the button below the fold on phone), once.
4. Publish (`icon` fitting the business), save the URL.
5. Ask: **looks right, go to review / change something** (offer the two changes you would most expect,
   for example "make it bolder" or "shorter page").

Revisions republish the same file path so the link never changes.

## Step 5 — Review

Goal: an honest list of what is wrong, ranked, with the user choosing what to fix.

1. Refresh the local render and gather evidence:
   ```bash
   python3 .claude/skills/design-site/scripts/build.py preview <page.html> <work>/preview
   node .claude/skills/design-site/scripts/check.cjs <work>/preview/index.html <work>/shots > <work>/check.json
   .claude/skills/impeccable/scripts/impeccable detect <work>/preview/index.html > <work>/detect.txt
   ```
   For the accessibility scan, serve `<work>/preview` on a local port and run the two `npx` commands
   from `.claude/skills/accessibility-scan/SKILL.md` (append `2>/dev/null` to the `ensure` command so
   its JSON parses), saving the output to `<work>/a11y.json`; stop the server and
   `npx -y @accesslint/chrome@latest stop` afterwards. If a tool cannot run, say so in the report —
   never report a check as passed that did not run.
2. Launch the three reviewers from `references/review.md` **in one message, in parallel** (Agent tool,
   `general-purpose`). Each gets the paths, not your opinion of the page.
3. Merge their findings: drop duplicates, drop anything that contradicts a decision the user already
   made, and rank by the order in `references/conversion-rules.md` (conversion blockers, then
   accessibility failures, then design quality, then polish).
4. Show the ranked list in chat: each finding one line, with the fix you would make. Then ask
   (multi-select): **apply all recommended / only the top group / let me pick / skip**.
5. Apply the chosen fixes to `page.html`, re-run `check.cjs`, republish, record `applied` and
   `declined` in the brief.

One review round by default. Offer a second only if the first changed the page substantially.

## Step 6 — Motion (optional)

Ask first: **none / subtle (Recommended for most pages) / expressive**. Skip in fast mode unless the
brand is playful or the user asked for animation.

If yes: read `.claude/skills/animate/SKILL.md` (and `.claude/skills/choreograph/SKILL.md` for a hero
entrance). One orchestrated moment on load plus feedback on things the visitor touches; nothing on
scroll for every section. Durations 100–300 ms, `prefers-reduced-motion` honoured, content visible
without the animation having run. Republish and ask: **keep / tone down / remove**.

## Step 7 — Ship

1. Run the pre-launch checklist in `references/conversion-rules.md` against `check.json` and the page.
   Report it as passed / failed / needs you (for example: real testimonials, real images, analytics).
2. Offer a first test plan in three lines, from `.claude/skills/ab-testing/SKILL.md`: the one
   hypothesis worth testing first, and how much traffic it needs.
3. Ask: **export now / keep refining / stop here** (the Artifact stays live either way).

On export:

```bash
python3 .claude/skills/design-site/scripts/build.py export <work>/page.html sites/<slug> <work>/brief.json
node .claude/skills/design-site/scripts/check.cjs sites/<slug>/index.html <work>/export-shots
```

Read one export screenshot to confirm the exported site matches the Artifact, then send the zip with
`SendUserFile` and tell the user what is in the folder and what still needs them (`needs_from_user`,
form destination, analytics, domain). `*.zip` is git-ignored in this repo, so the folder is what gets
committed; commit only if the user asks.

The export is a full replacement of `sites/<slug>/`. If that folder already exists and was edited by
hand since the last export, say so and ask before overwriting.

## Adding a page to an existing site

One run designs one page. For a second page (`/design-site resume <slug>` then "add a pricing page"),
reuse `look` and the header/footer from the existing `page.html`, skip step 3, and run steps 1–2 and
4–7 for the new page as `page-<name>.html`, exported as `<name>.html` beside `index.html`.
