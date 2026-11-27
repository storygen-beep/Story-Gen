# Conversion rules

Condensed from `docs/design/web-design-conversion-playbook.md`, which carries the sources and caveats.
These are the rules a page is built against in step 4 and reviewed against in step 5.

## Order of importance

1. The right visitor sees a message that matches what they clicked.
2. The offer is obvious within ten seconds, on the first screen.
3. Friction and anxiety are removed.
4. Polish.

A weak or unclear offer is not rescued by anything lower on the list. Rank review findings in this order.

## Build-time rules

**First screen**
- The headline states the outcome in plain words. A stranger can say what is sold after five seconds.
- For paid traffic, the headline repeats the ad's promise or keyword.
- One primary action, visible without scrolling on a 375 px phone, marked `data-cta="primary"`.
- The button label says what happens next ("Start my first box"), not "Submit" or "Learn more".
- One real picture of the product or its interface. No abstract decoration standing in for it.
- A short trust line near the button if the brief has one (rating and count, "no card required").

**Page**
- One goal per page. Secondary links (log in, docs) are visually quiet. The primary action repeats
  at the end of the page and uses the same label throughout.
- Proof sits near the top and beside claims: specific testimonials with name and role, review rating
  with count, recognisable logos, real numbers. Only what the brief supplies; otherwise a marked
  placeholder.
- Subheads carry the argument on their own, because most visitors read only headings.
- Copy at about a 6th-grade reading level (`readingGrade` ≤ 8 in the checker); short sentences.
- Objections answered before the final button: price, security, cancellation, time to value.
- Full price visible before commitment. No surprise costs. Guarantee next to the buy button.
- No auto-rotating carousel. No popup on arrival.

**Forms**
- Ask for the minimum. Every extra field costs conversions; phone, age, dropdowns and long text
  boxes cost the most.
- Correct `type` and `autocomplete` on every field, a visible `<label>` for each.
- Validate when the visitor leaves a field, not while they type. Errors say how to fix it.
- No forced account creation for a purchase.

**Looks and usability**
- Familiar structure for the category (logo, navigation, pricing where people expect them), distinctive
  craft in type, colour and detail. Simple and familiar is rated most appealing within 50 ms.
- Body text 50–75 characters per line (`longestBodyLineChars` ≤ 80), line-height ≥ 1.5.
- One spacing scale in 4/8 px steps.
- Contrast: text 4.5:1, large text and control borders 3:1. Visible keyboard focus.
- Tap targets at least 24×24 px; primary actions at least 44 px tall.
- Motion 100–300 ms, `prefers-reduced-motion` respected, nothing essential hidden until animated.
- No horizontal scroll at 375 px.

**Speed**
- Images sized to their box, with `width`/`height` set so the layout does not jump, lazy-loaded below
  the first screen. Two font families at most, with `display=swap`.
- Targets once hosted: largest element painted < 2.5 s on mobile, layout shift < 0.1.

**AI-generated tells to avoid** (unless the user asked for one)
Purple-to-blue gradients; Inter or system font as the only face; cream background with serif headline
and terracotta accent; near-black with one acid-green accent; an ALL-CAPS label above every heading;
identical rounded cards with the same soft shadow; cards inside cards; big number with small label stat
rows as the hero; 01/02/03 markers on content that is not a sequence; fade-and-slide-up on every
section; an arrow on every button; emoji as icons; grey text on a coloured background.

## Page anatomy (landing page)

Use what the brief can fill; drop the rest.

1. Hero — headline, subhead, primary button, product picture, trust line
2. Proof strip — logos or rating and count
3. Outcomes — up to three benefits, each a subhead that reads as a claim
4. How it works — real steps with real screenshots
5. Testimonials — specific, attributed
6. Pricing — total visible, guarantee by the button
7. Questions — the objections
8. Final action — the primary button again, nothing competing

## Things with no solid evidence either way

Button colour (contrast with the page matters, the hue does not), the exact button wording, whether to
highlight a "recommended" plan, how many pricing tiers. Make a sensible choice, say it is a judgement
call, and put it in the step 7 test plan rather than presenting it as settled.

## Pre-launch checklist (step 7)

Mechanical — read from `check.json`:
- [ ] `h1Count` is 1 and the headline matches the brief
- [ ] `primaryCtaAboveFold` true on phone and desktop; one label in `primaryCtaLabels`
- [ ] `primaryCtaSize.height` ≥ 44
- [ ] `readingGrade` ≤ 8
- [ ] `horizontalOverflowPx` 0 at every width
- [ ] `imagesMissingAlt` 0, `fieldsMissingAutocomplete` 0, `targetsUnder24px` empty
- [ ] `longestBodyLineChars` ≤ 80 on desktop
- [ ] `fontsFailed` empty, `consoleErrors` empty
- [ ] accessibility scan: no critical or serious violations
- [ ] `impeccable detect`: no findings, or each one a deliberate choice recorded in `decisions`
- [ ] `designmd lint` on the site's `DESIGN.md`: no errors, no contrast warnings

Judgement — look at the page:
- [ ] Five-second test: headline and picture alone say what is sold
- [ ] Proof is real and near the top; no placeholders left
- [ ] Price and guarantee visible before the commitment
- [ ] None of the AI-generated tells

Needs the user:
- [ ] Real images and testimonials supplied
- [ ] Form or button wired to a real destination
- [ ] Analytics and a conversion event in place before launch
