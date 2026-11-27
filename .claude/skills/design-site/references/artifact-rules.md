# Artifact rules for design-site pages

Load the `artifact-design` skill before the first publish; it is the full contract. This file is the
subset that matters for a website design, plus the conventions the export script depends on.

## The file is a fragment

- No `<!doctype>`, `<html>`, `<head>` or `<body>`. Start the file with:
  ```html
  <title>Site Name</title>
  <meta name="claude:viewport-fit-sides" content="cover">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">
  <style> ... </style>
  ```
- The title is the site's name, two to four words. No "landing page" or "option 2" in it.
- All CSS in `<style>` blocks, all page JS in inline `<script>` blocks. `build.py export` moves them to
  `css/styles.css` and `js/main.js`, so do not write scripts that depend on where in the document they
  sit (`document.write`, `document.currentScript`).

## What loads and what does not

- Fonts: Google Fonts only, with a real fallback stack.
- Scripts: only cdnjs.cloudflare.com (preferred), cdn.jsdelivr.net/npm, unpkg.com, cdn.tailwindcss.com,
  code.jquery.com, pinned to an exact version. Most pages need none.
- Images: no external image URLs load. Use inline SVG, CSS, or `data:` URIs. The export script turns
  every `data:` image into a real file under `assets/`.
- No iframes or embeds (video, maps). Use a poster image with a play button as a stand-in and note it
  in `needs_from_user`.

## Pictures before the user has supplied any

In order of preference:
1. The product's own interface, built in HTML/CSS as a small realistic mock-up.
2. An inline SVG illustration specific to the subject.
3. A marked placeholder box (`data-placeholder="hero photo: barista handing over a bag"`) sized to the
   final image, with the description visible.

Never a stock-photo URL (it will not load) and never an abstract gradient blob standing in for the
product.

## Layout rules the artifact enforces

- Side gutter on the outer wrapper (or each full-width band's inner wrapper):
  `padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));`
  with vertical padding via `padding-block`.
- No horizontal page scroll at 375 px. Rows wrap or stack.
- Size the hero to its content, not `100vh`.
- Everything readable is visible at rest; nothing waits at `opacity: 0` for a scroll observer.

## Colour and theme

A website design commits to one visual world, so the page is single-theme **by choice**: define every
colour as a token on `:root`, set `body { background: var(--bg); color: var(--fg) }` explicitly, and
add `color-scheme: dark` on `:root` if the design is dark. Do not add dark-mode blocks unless the brief
asks for a site that supports both.

## Things that behave differently in an artifact

- Forms cannot submit anywhere. Handle `submit` with `preventDefault()` and show the success state
  in the page. Record the real destination as a `needs_from_user` item.
- `mailto:` and `tel:` links are unreliable; show the address or number as text as well.
- No `alert`/`confirm`/`prompt`, no downloads, no print dialog.
- Links to other sites open in a new tab. In-page links use plain `#section-name` anchors.

## Conventions this skill adds

- `data-cta="primary"` on every instance of the main action button.
- `data-placeholder="what goes here"` on every stand-in for content the user still owes.
- A stable `id` on every form control and every section that navigation links to.

## The options page (step 3)

One artifact, three directions, switched by tabs:

```html
<title>Site Name Directions</title>
<nav class="ds-tabs" aria-label="Design directions"> <button data-opt="a" aria-pressed="true">A · Name</button> ... </nav>
<section class="opt opt-a"> hero + next section </section>
<section class="opt opt-b" hidden> ... </section>
<section class="opt opt-c" hidden> ... </section>
```

- Each direction's tokens live under its own class (`.opt-a { --bg: ...; --fg: ...; --accent: ... }`)
  and every rule for that direction is prefixed with the class, so the three never bleed into each other.
- Toggle with the `hidden` attribute. Remember the last tab in `localStorage` inside try/catch.
- The tab bar is the only shared chrome: keep it small, neutral and sticky
  (`top: env(safe-area-inset-top, 0px)`), with one line under each name saying who the direction suits.
- Same headline, subhead and button in all three, so the user compares looks and not words.
