# Web Design That Converts — Playbook and Skill Stack

Research compiled 2026-11-27. Every number below carries its source. Tags: **[OLD]** = data before 2020,
**[VENDOR]** = a company reporting on its own platform or customers, **[GAP]** = no rigorous public evidence found.

---

## 1. The core model: why pages convert

Three frameworks agree on the order of importance. Use them as a diagnostic, not as math.

- **LIFT (WiderFunnel / Conversion.com):** the value proposition is the centre. Drivers: *relevance*, *clarity*,
  *urgency*. Inhibitors: *anxiety*, *distraction*. Nothing compensates for a weak value proposition.
  https://conversion.com/?p=4613
- **MECLABS C = 4m + 3v + 2(i − f) − 2a:** motivation > value clarity > (incentive − friction) > anxiety. The weights
  are a heuristic, not fitted data — but the ordering is the lesson: fixing friction matters less than a clear, wanted
  offer shown to motivated traffic.
- **Fogg B = MAP:** a behaviour happens only when Motivation, Ability (ease) and a Prompt (CTA) meet at the same moment.
  https://behaviormodel.org/

**Practical reading:** first get the right visitor (message match), then make the offer obvious in ten seconds, then
remove friction and anxiety, then polish. Most teams do this in reverse.

---

## 2. The 15 highest-leverage rules (ranked)

1. **No surprise costs.** Extra costs are the #1 abandonment reason (40%); not seeing the total up front is another
   12%. Baymard — https://baymard.com/lists/cart-abandonment-rate
2. **Value proposition in ten seconds, on the first screen.** The first screen gets ~57% of viewing time; leave risk is
   highest in the first 10 s. NN/g [OLD] — https://www.nngroup.com/articles/scrolling-and-attention/ ·
   https://www.nngroup.com/articles/how-long-do-users-stay-on-web-pages/
3. **Fast on mobile.** −0.1 s mobile load = +8.4% retail / +10.1% travel conversion (Deloitte for Google [VENDOR]);
   a 1 s site converts 2.5–3× a 5 s site (Portent [VENDOR]); bounce probability +32% going from 1 s to 3 s
   (Google/SOASTA [OLD]). https://web.dev/case-studies/milliseconds-make-millions ·
   https://www.portent.com/blog/analytics/research-site-speed-hurting-everyones-revenue.htm
4. **Guest checkout / no forced account.** 18% of abandonment. Baymard.
5. **Cut fields.** Ideal checkout is 7–8 fields (12–14 elements) vs ~15 fields (23.5 elements) on average. Delete
   optional fields; Expedia dropped one confusing "Company" field and reported ~$12M/yr [OLD, VENDOR]. Phone, age,
   dropdowns and textareas cost the most (HubSpot 40K pages [OLD, VENDOR]).
6. **Show reviews.** 5 reviews = +270% purchase likelihood vs none; +380% on higher-priced items. Ratings peak at
   4.0–4.7 stars — a perfect 5.0 looks fake. Spiegel Research Center —
   https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/
7. **Message match.** The landing headline should repeat the ad's promise/keyword. Dynamic keyword replacement lifted
   trial signups 31.4% [VENDOR]. https://unbounce.com/landing-page-examples/built-using-unbounce/dynamic-text-a-b-test/
8. **Write plainly and short.** 5th–7th grade reading level converts at 11.1% vs 5.3% for professional-level copy;
   word count, reading time and 3+-syllable words all correlate negatively (correlation, not experiment). Unbounce
   2024 [VENDOR] — https://unbounce.com/conversion-benchmark-report/
9. **Reduce anxiety at the payment step.** 19% abandon from distrust of card handling. Recognisable marks
   (Norton/PayPal tier), a real address, real people, findable contact. Baymard · Stanford credibility guidelines
   [OLD] — https://credibility.stanford.edu/guidelines/index.html
10. **Fix checkout UX as a whole.** Estimated +35% conversion upside for an average large e-commerce site; 64% of leading
    sites rate mediocre or worse. Baymard estimate — https://baymard.com/blog/current-state-of-checkout-ux
11. **Inline validation — after the field is finished, never mid-typing.** +22% success, −42% completion time (small
    2009 lab test [OLD]). https://alistapart.com/article/inline-form-validation-in-web-forms/
12. **Stable layout and fast main content (CLS, LCP).** Redbus CLS 1.65 → 0: mobile conversion +80–100%; Vodafone LCP
    −31%: +8% sales [VENDOR]. https://web.dev/case-studies/vitals-business-impact
13. **No auto-rotating carousels for key offers.** ~1% of visitors click, 84–89% of those on slide 1 [OLD];
    auto-rotation triggers banner blindness. https://www.nngroup.com/articles/auto-forwarding/
14. **Anchor/decoy pricing tiers.** The Economist decoy moved the bundle share from 32% to 84% (classroom study
    [OLD] — test it). https://en.wikipedia.org/wiki/Decoy_effect
15. **Test, don't copy.** Of 653 GoodUI pattern tests only ~26% won outright. https://goodui.org/patterns/

### Myths to stop repeating
- **"Red/orange buttons convert best."** The famous test was ~2,000 visits; contrast and isolation won, not hue.
  https://cxl.com/blog/which-color-converts-the-best/
- **"Fewer choices always convert better."** Meta-analysis of 50 experiments: average choice-overload effect ≈ 0.
  https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html — keep *one goal per page* for distraction reasons
  (LIFT), not because of the jam study.
- **"Nobody scrolls."** ~43% of viewing time is below the fold.
- **"5.0 stars is best."** Peaks at 4.0–4.7.

### Benchmarks (Unbounce 2024, 41K pages [VENDOR])
Median landing-page conversion across industries **6.6%** (range 3.8–12.3%). SaaS 3.8%, e-commerce 4.2% (top quartile
≥ 11.4%), professional services 6.1% (top quartile ≥ 14.1%). Desktop still converts ~1.5–2× mobile
(Dynamic Yield 3.0% vs 4.4%; Adobe BF 2024 3.3% vs ~6.5% [VENDOR]).

### Evidence gaps [GAP]
CTA wording ("Get started" vs "Start free trial"), highlighted "recommended" pricing plan, number of tiers, and
5-second-test scores have no rigorous public conversion study. Test them on your own traffic.

---

## 3. UI fundamentals: looking good *is* converting

- **First impressions are visual and fast.** Visual-appeal ratings after 50 ms match those after longer viewing
  (Lindgaard 2006 [OLD]). Google Research 2012: within 17–50 ms, **low visual complexity + high prototypicality**
  (looks like its category) is rated most appealing. Be familiar in structure, distinctive in craft.
  https://research.google/blog/users-love-simple-and-familiar-designs-why-websites-need-to-make-a-great-first-impression/
- **Looks drive credibility.** 46.1% of people judged site credibility partly on design (54.6% for finance) —
  Stanford 2002 [OLD]. Aesthetic-usability effect: attractive UIs are *perceived* easier to use (Kurosu & Kashimura).
  Caveat: polish hides usability problems in testing.
- **Typography.** Body line length 50–75 characters (`max-width: ~70ch`; Baymard sees fatigue at 100+). Line-height
  ≥ 1.5. One display face + one text face is enough.
  https://baymard.com/blog/line-length-readability
- **Spacing.** One scale in 4/8-px steps (Material 3). Consistent rhythm reads as quality.
- **Contrast (WCAG 2.2 AA).** Text 4.5:1, large text (≥ 24 px, or ≥ 18.5 px bold) 3:1, UI boundaries/focus rings
  3:1. Do not round: 4.499:1 fails. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- **Touch targets.** WCAG 2.5.8 AA minimum 24×24 CSS px; design to Apple 44 pt / Material 48 dp for primary actions.
- **Motion.** ~100 ms micro-feedback, 200–300 ms modals/larger changes, ≤ 400 ms big moves; ~500 ms feels like drag.
  Always honour `prefers-reduced-motion`. https://www.nngroup.com/articles/animation-duration/
- **Response time.** Doherty threshold: keep interactions under ~400 ms or show progress.

### AI-slop tells (what makes a generated site look generated)
From Anthropic's frontend-design skill, impeccable and ui-ux-pro-max:
purple-to-blue or gradient washes; Inter/system font everywhere; the newer default too — cream background + serif
display + terracotta accent, or near-black + one acid-green accent; tracked-out ALL-CAPS eyebrow above every heading;
identical rounded cards with the same soft shadow; cards inside cards; big-number + tiny-label stat rows;
01/02/03 markers; fade-and-slide-up on every section; "→" on every button; emoji used as icons; gray text on colored
backgrounds; bounce/elastic easing; vague headline + generic CTA.

---

## 4. UX fundamentals: usable *is* converting

- **NN/g 10 heuristics** — visibility of status; match the real world; user control; consistency; error prevention;
  recognition over recall; efficiency; minimalist design; clear error recovery; help.
  https://www.nngroup.com/articles/ten-usability-heuristics/
- **Laws of UX** that matter most on a landing page: **Jakob** (work like sites they already know — put nav, logo,
  pricing where people expect them); **Fitts** (primary CTA large and close to where attention is); **Hick** (fewer,
  clearer decisions per screen); **Von Restorff** (the primary CTA is the one element that looks different).
  https://lawsofux.com/
- **Scanning.** People F-scan walls of text; with strong, descriptive subheads they layer-cake scan (headings only),
  which NN/g calls the most effective pattern. Write subheads that carry the argument on their own.
  https://www.nngroup.com/articles/layer-cake-pattern-scanning/
- **Mobile.** 75% of mobile e-commerce sites rate only "mediocre" (Baymard 2026). Thumb-reachable CTA, no hover-only
  affordances, input types that open the right keyboard, autofill attributes on every form field.

---

## 5. Page anatomy that converts (landing page)

1. **Hero** — headline that states the outcome in plain words (matches the ad), one-line subhead with *how*, one
   primary CTA, one real product image/UI (not an abstract blob), a trust micro-line (rating, customer logos, or
   "no card required").
2. **Proof strip** — recognisable logos or rating + review count.
3. **Problem → outcome** — 3 benefit blocks, each a subhead that reads as a claim.
4. **How it works** — 3 steps, real screenshots.
5. **Social proof** — specific testimonials with name, photo, role; numbers over adjectives.
6. **Objection handling / FAQ** — price, security, cancellation, time to value.
7. **Pricing** (if relevant) — total visible, anchor tier, annual/monthly toggle, guarantee near the button.
8. **Final CTA** — repeat the primary action; nothing competing with it.

One page = one goal. Secondary links (docs, login) stay visually quiet.

---

## 6. Recommended Claude Code skill stack

Installed in this repo:

| skill | role |
|---|---|
| `awesome-design-skills` (bergside, 67 styles) | visual style library — pick a look, apply its tokens and gates |

Recommended next, in priority order (verified on GitHub 2026-11-27; star counts approximate):

| # | skill | what it adds | install |
|---|---|---|---|
| 1 | **anthropics/skills → frontend-design** | official baseline; strong anti-slop guidance | copy `skills/frontend-design` into `.claude/skills/` |
| 2 | **pbakaus/impeccable** (~118k★) | 24 commands: `critique`, `audit`, `polish`, `bolder`, `distill`, `typeset`… + 62-rule slop detector | `npx impeccable install` then `/impeccable init` |
| 3 | **coreyhaines31/marketingskills** | the *conversion* half: `cro`, `copywriting`, `signup`, `pricing`, `popups`, `ab-testing`, `marketing-psychology` | copy chosen `skills/*` folders |
| 4 | **nextlevelbuilder/ui-ux-pro-max-skill** (~155k★) | searchable DB: styles, 194 palettes, 74 font pairs, 141 UX rules, per-stack guidance | copy `.claude/skills/ui-ux-pro-max` |
| 5 | **vercel-labs/agent-skills → web-design-guidelines** | audits UI code against Vercel's interface guidelines (a11y + UX) | copy `skills/web-design-guidelines` |
| 6 | **emilkowalski/skills** (~60k★) | motion and interaction craft: `animate`, `review-animations`, `break-ui`, `apple-design` | `npx skills@latest add emilkowalski/skills` |
| 7 | **AccessLint/skills** | WCAG 2.2 scan / audit / fix / regression diff | `npx skills add AccessLint/skills` |
| 8 | **Leonxlnx/taste-skill** (~122k★) | full "company-site" builder with browser checker + finish gate; heavy (~40 MB photos) | copy `skills/taste-skill` |
| 9 | **anthropics/knowledge-work-plugins → design** | `design-critique`, `ux-copy`, `accessibility-review`, `user-research` | `claude plugin marketplace add anthropics/knowledge-work-plugins` |
| 10 | **plugin87/ux-ui-agent-skills** | 26 skills + design-critic agent, 52 browser/file gates | `/plugin marketplace add plugin87/ux-ui-agent-skills` |

Situational: official **shadcn** skill (`pnpm dlx skills add shadcn/ui`) for shadcn stacks; **figma/mcp-server-guide**
for Figma → code (note: fetches design data at runtime, a prompt-injection surface); **microsoft/playwright-cli**
for screenshot QA (this repo already has `playwright-skill`).

**Don't stack overlapping "taste" skills blindly.** frontend-design, taste-skill, impeccable and ui-ux-pro-max all
carry aesthetic opinions and they produce different results from the same prompt. Pick one as the builder, use the
others as reviewers.

### Suggested workflow
1. **Brief** — audience, traffic source, single conversion goal, offer, proof assets (`cro` + `copywriting`).
2. **Style** — pick a direction from `awesome-design-skills` (or ui-ux-pro-max palettes/fonts).
3. **Build** — `frontend-design` as the builder.
4. **Critique** — `impeccable critique` + `web-design-guidelines` audit.
5. **Accessibility** — AccessLint scan, fix contrast/targets/focus.
6. **Speed** — Lighthouse/CWV: LCP < 2.5 s, CLS < 0.1, INP < 200 ms.
7. **Screenshot QA** — Playwright at 375 / 768 / 1440 px.
8. **Ship and test** — `ab-testing`: one hypothesis at a time, enough traffic per variant.

---

## 7. Pre-launch checklist

- [ ] Headline states the outcome; a stranger can say what you sell after 5 seconds
- [ ] Headline matches the ad / search intent driving traffic
- [ ] One primary CTA, visually unique, repeated at the end
- [ ] Real product imagery; proof (rating, logos, testimonials) above or right below the fold
- [ ] Copy at ~6th-grade reading level; subheads readable alone
- [ ] Full price / total visible before commitment; guarantee next to the button
- [ ] Form: minimum fields, correct input types + autocomplete, validation after blur, guest option
- [ ] Trust at the payment step: recognisable marks, real contact, policy links
- [ ] No auto-rotating carousel; no popup on entry
- [ ] Contrast ≥ 4.5:1 text, ≥ 3:1 UI; targets ≥ 24 px (44 px for primary); visible focus
- [ ] `prefers-reduced-motion` honoured; animations ≤ 300 ms
- [ ] LCP < 2.5 s on mobile 4G; CLS < 0.1; images sized and lazy below the fold
- [ ] None of the AI-slop tells from §3
- [ ] Analytics + conversion event firing before launch
