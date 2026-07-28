# Player-Guide PDF Pipeline

**Status:** proof of concept, shipped and working. Branch `guide-pdf`, commit `323a96d`.
**Built:** 2026-07-26. **Proven against:** Vesper v0.1.5.

This document exists because the pipeline was built as a *dummy* — a deliberate
proof that a Patreon-grade guide PDF can be produced from this repo — and a dummy
is only worth anything if the reasoning behind it survives. Everything below was
measured on this machine or read out of the code. Where something is unverified it
says so.

---

## 1. What this is

A renderer. You hand-write a guide in markdown; it produces a print-ready PDF with
a cover, a table of contents with real page numbers, running headers, a PDF outline,
and styled tables.

```
games/<slug>/guide/guide.md          ← authored prose (tracked in git)
scripts/guide_styles/dossier/        ← template.html + style.css (game-agnostic)
apps/game_generation/management/commands/build_guide.py
        ↓
games/<slug>/guide/<slug>_guide_v<version>.pdf   ← build artifact (gitignored)
```

```bash
python manage.py build_guide --game vesper
```

### What it is NOT

It does not read the game. It never opens the canvas graph, never walks the flag
chain, never touches `v2.py` or `package_from_toml`. The single thing it reads from
the game is the version stamp (§7).

That is a decision, not a limitation — see the next section.

---

## 2. The decision: authored, not generated

The obvious design is to generate the guide from `7_final_game.toml`. It was
investigated and rejected. Both halves of the reasoning matter.

**The data supports it further than expected.** Vesper's merged TOML carries 25
locations with lock conditions, 12 NPC schedule rows, 133 canvases / 255 choices with
typed conditions and effects, 56 flags, 27 distinct numeric trait gates, and 33 quest
cards already holding author-written coaching text. The flag graph yields 85
setter→reader edges and sorts topologically with no cycles.

**And it still isn't a walkthrough.** 53 of 128 non-dev canvases have no flag edge at
all — they are gated on traits, schedules or RNG. A topological sort of the remainder
is a *partial order*, not a route. And 24 of Vesper's 26 declared traits are
`hidden = true` with no player-facing label, so a player-facing document would need an
invented name-mapping layer that exists nowhere.

**The genre agrees.** Four official Patreon/itch walkthrough PDFs were extracted to
text (FreshWomen, Lewd Island, My Pleasure S1, Harem in Another World). All four are
hand-authored prose. None is generated. Their shared skeleton is in §9.

So: the numbers are authored *by hand* and kept honest by the version stamp. If a
threshold changes in the game, the guide is wrong until someone edits it. That is an
accepted cost — the alternative was a large extraction layer that still could not
write the half of the document that matters.

---

## 3. Engine evaluation

Four candidates each rendered the same test document — cover, dot-leader TOC, heading
hierarchy, zebra table, a real portrait, hyperlink, running header, page counters —
and the resulting pages were rasterised and **looked at**. A render that throws no
errors is not evidence of anything.

| | works here | TOC w/ page numbers | PDF bookmarks | render | adoption cost |
|---|---|---|---|---|---|
| **WeasyPrint 69** ← chosen | yes | ✅ `target-counter` + `leader()` | ✅ 3-level | 0.95 s | `brew install pango` + a dyld var |
| Chromium 149 (Playwright) | yes | ❌ silently bare | ✅ *only* with `tagged=True` | 1.9 s | new dep + possible browser download |
| Typst 0.15.0 | yes | ✅ | ✅ | 0.15 s | self-contained wheel; new markup language |
| fpdf2 2.8.7 | yes | hand-rolled | ✅ | 0.31 s | 277 lines of Python for a worse document |

**WeasyPrint won** because it was the only engine that produced a complete, correct
document with **zero post-processing**, from HTML/CSS we can already write.

### Two pieces of common knowledge that are now false

- *"Chromium can't do CSS page counters."* It can. Chrome 131 (Oct 2024) shipped
  `@page` margin boxes; Chromium 149 rendered `counter(page) " / " counter(pages)`
  correctly. What it still does **not** do is `target-counter()` (so a TOC ships with
  no page numbers) or `string-set` running headers — and it fails at both *silently*,
  which is the real hazard.
- *"WeasyPrint needs cairo and gdk-pixbuf."* Stale. v69 dlopens only
  gobject/pango/harfbuzz/fontconfig/pangoft2.

### Why not Typst

Nothing wrong with it — it passed every feature test, installs as a self-contained
30.5 MB wheel with no system libraries at all, and rendered 6× faster. **It is the
right answer if this ever has to run in Docker or CI**, because it sidesteps the
entire native-library problem below. It was passed over only because HTML/CSS is a
language we already use and the stylesheet doubles as something we could serve on the
web.

---

## 4. The macOS native-library problem

WeasyPrint loads pango/harfbuzz through `ctypes`. On this machine those live in
`/opt/homebrew/lib`, which is not on the default dyld search path, so a bare import
fails:

```
OSError: cannot load library 'libgobject-2.0-0'
```

The fix, in `build_guide.py`, before the import:

```python
if sys.platform == "darwin":
    os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")
```

**This must be done inside Python.** macOS SIP strips `DYLD_*` across an exec of a
protected system binary, so exporting it in a wrapper shell script, or invoking the
renderer through `/usr/bin/env`, `/bin/sh` or `/usr/bin/time`, silently does nothing
and you get the original error back. This was verified with a bogus-path control: the
var set to `/nonexistent/lib` fails, set to `/opt/homebrew/lib` succeeds — so the
environment variable is demonstrably what does the work.

Related environment facts:

- The repo venv is a **uv-managed standalone CPython 3.12.11 with no `pip` binary**.
  Install with `uv pip install --python venv/bin/python <pkg>`; a bare `pip install`
  fails confusingly.
- Its `ctypes` cannot resolve homebrew libraries on its own (`find_library('pango-1.0')`
  → `None`), which is exactly why the var is needed. Homebrew's own python3.12 does not
  need it. **Pin the interpreter as well as the package** — the same WeasyPrint version
  behaves differently across three Pythons on this one machine.
- Dependencies are declared in a `requirements/` **directory**, not a root
  `requirements.txt`. `pyproject.toml` declares none; `poetry.lock` is an empty stub.
- The Dockerfile installs `requirements/development.txt` on `python:3.10-slim`, where
  WeasyPrint additionally needs `apt-get install libpango-1.0-0 libpangoft2-1.0-0`.
  **That step is not in the Dockerfile.** Untested — this is currently an author-local
  tool.

---

## 5. Architecture

Three files, one direction of flow, no shared state.

### `build_guide.py` — the command

```
guide.md ──► markdown.Markdown(extensions) ──► body HTML + md.toc + md.Meta
                                                      │
7_final_game.toml ──► [project] version/release ──────┤
                                                      ▼
                        template.html  ──► slot substitution ──► one HTML string
                                                      │
                                                      ▼
                        WeasyPrint(base_url=guide dir) ──► PDF
```

Markdown extensions, and why each is load-bearing:

| extension | buys |
|---|---|
| `meta` | the `Key: value` front matter block |
| `tables` | the guide is mostly threshold tables |
| `admonition` | `!!! warning` / `!!! spoiler` callout boxes |
| `toc` | heading anchors — CSS supplies the page numbers, not this |
| `attr_list` | `{: .class }` escape hatch for one-offs |
| `sane_lists`, `smarty` | list behaviour; real quotes and dashes |

**Slot substitution is plain `str.replace`, not `str.format`.** The template carries
literal CSS and HTML braces; any brace-based formatter chokes on them. Slots:
`{{title}} {{subtitle}} {{version}} {{release}} {{byline}} {{cover}} {{stylesheet}}
{{toc}} {{body}}`.

`base_url` is set to the guide's own folder, so relative image paths resolve exactly
as they do when previewing the markdown in an editor.

### `scripts/guide_styles/dossier/` — the design

`template.html` is the page furniture (cover, contents sheet, legend). `style.css` is
~830 lines of print CSS. Swapping styles is a `--style` flag; adding one is a new
directory with those two filenames.

---

## 6. Authoring conventions for `guide.md`

### Front matter

```
Title: Vesper
Subtitle: The Official Guide
Version: 0.1.5
Release: 2026-07-25
Cover: ../output/videos/portraits/wren_cover.jpg
Byline: Written by the developer. Distributed to patrons.
```

`Version` and `Release` are **overridden** by the game TOML when `--game` is passed.
They are a fallback for standalone renders.

### Structure

- `#` (h1) = a chapter. **Forces a page break** and becomes a level-1 PDF bookmark and
  the running header.
- `##` / `###` = sections, numbered `4.2`-style in the left rail, level-2 bookmarks.
- Every heading lands in the TOC with a dot leader and a resolved page number.

### The one convention that matters most

**Anything in backticks becomes a mono chip.** Flags, thresholds, band values:

```markdown
| **Charge: Critical** | `0–24` | She's running out. |
| Earn the office | `relation ≥ 21` | He waves you into the back office |
Taking the work sets `renner_hired`.
```

This is how the genre's "expose the hidden numbers" requirement gets satisfied by a
typing habit rather than by styling decisions. Chips make load-bearing values pop out
of running prose, and the legend on the contents sheet teaches the reader the code
before they meet it.

### Callouts

```markdown
!!! warning "The one gate that will strand you"
    Condition below 40 blocks travel to the Reach.

!!! spoiler "Read at your own risk"
    Every gate and threshold in the build is printed here.
```

`warning` renders as a tinted operational caution; `spoiler` as a sealed reversed-out
black block. They are distinct **in kind**, not merely in colour, so a reader skimming
knows which is which at a glance.

### Images

Point at already-tracked media so the guide renders from a clean clone:

```markdown
![Cover: the analyst](../output/videos/portraits/wren_cover_analyst.jpg)
*Analyst's grays. What the tower sees.*
```

Media is globally gitignored **except** `games/vesper/output/videos/**` and
`games/the_inheritance/output/videos/**`. For any other game, a portrait-bearing guide
is machine-local only.

---

## 7. Versioning and distribution

### The stamp cannot drift

`[project] version` and `release_date` in `games/<slug>/toml_phases/7_final_game.toml`
already drive the in-game sidebar footer. `build_guide` reads the same two fields, so
a published guide cannot claim a build it wasn't written against, and the output
filename carries it: `vesper_guide_v0.1.5.pdf`.

### ⚠️ The repo is public

`origin` is `https://github.com/storygen-beep/Story-Gen`, `"visibility":"PUBLIC"` —
the same repo that serves the GitHub Pages game portal. **A guide PDF committed under
`games/` is a free download and the Patreon gate stops meaning anything.**

`.gitignore` therefore carries `*.pdf` with the reason written next to it. Commit the
markdown; upload the PDF. This also avoids multi-megabyte binary diffs on every
rebuild — PDFs embed a `CreationDate`, so no two builds are byte-identical.

### The CTA already ships

The Patreon URL is hardcoded in the engine's sidebar widget
(`apps/game_generation/twee_comprehensive/generators/v2.py:16010`), so an in-game
"the guide is on Patreon" pointer costs nothing to add.

### Watermarking: skipped, deliberately

Per-patron stamping is cheap to build (~0.06 s/copy with `pypdf`, outline and links
survive). It was skipped because no evidence was found that anyone in this genre does
it, and patron cheat codes are demonstrably reposted publicly within a version cycle.
Gate on tier for revenue; assume leakage for planning. Revisit if a leak actually
costs something.

---

## 8. The visual design, and why

Three treatments were built against identical content — a diegetic company dossier, a
premium editorial book, and a dark terminal-noir — then scored by two judges with
different lenses (readability-as-reference; design quality as a paid product). Both
independently picked **the dossier**.

The guide presents itself as a leaked internal Vance Dynamics compliance file. It was
the only treatment where every element descends from one idea, the only one with no
generic-AI-document tells (one accent colour, no unmotivated gradients, no decorative
emoji, no competing radii), and the only identity that says something about *this*
game rather than about a genre.

Both judges named the same defect — the cover was a page of form-text that read as a
filed tax return at thumbnail size, which is the first thing a patron ever sees. Two
borrows were applied:

1. **The full-bleed cover** from the editorial treatment — art at trim, a motivated
   five-stop legibility scrim (dark only where type sits, clear across the middle so
   the subject is never veiled), wordmark set in the dossier's own Charter rather than
   an imported display face. The control form moved to the contents sheet.
2. **Mono chips on band values** from the noir treatment — achieved as a content
   convention (§6) rather than a stylesheet rule, so it generalises.

### CSS Paged Media features actually in use

`@page` named pages · margin boxes · `counter(page)`/`counter(pages)` ·
`string-set` + `string()` running headers · `target-counter(attr(href url), page)` +
`leader('.')` · `bookmark-level` / `bookmark-label` · `thead { display:
table-header-group }` · `break-before/inside/after` · `orphans`/`widows`

### Layout gotchas found by rendering, not by reading

Each of these is commented at the point of use in `style.css`:

- **`text-indent` inherits into `::before`.** The hanging rail uses `padding-left` plus
  a negative `text-indent`; that indent inherits into the inline-block pseudo-element
  and throws the section number off the left edge of the sheet. Every `::before` resets
  `text-indent: 0`.
- **A negative `text-indent` shortens the line box**, so `leader()` stops short of the
  right edge instead of running to the folio. TOC anchors carry no hanging indent.
- **A float beside the TOC collides with the leaders** for the same reason. Nothing may
  float next to `leader()` content.
- **`hyphenate-character`.** The hyphenator's default break character is U+2010, which
  Charter lacks — every hyphenated word was drawing its hyphen out of Hiragino Mincho.
  Forced to the ASCII hyphen-minus. *Audit the PDF's embedded font table; do not trust
  the eye.*
- **`break-inside: avoid` on a block that misses the page foot exiles it to a page of
  its own.** The legend missed by ~40 pt and took a whole sheet for four rows; fixed by
  measuring the gap off the PDF and tightening the margin.

### Engine limits worth knowing

- **Colour emoji render badly in WeasyPrint** — undersized and off-baseline. Vesper's
  sidebar meter bands *are* emoji (`7_final_game.toml:119`). A print guide should use
  text labels regardless, so this never bit, but do not build a design that needs them.
  Chromium renders them correctly if you ever must.
- **WebP explodes 8–11× inside a PDF** — there is no WebP filter in the format, so it
  is stored as a raw bitmap and no optimisation flag touches it. Convert to JPEG first.
  JPEG passes through byte-identical.
- `write_pdf(optimize_images=True, jpeg_quality=80, dpi=150)` measured a ~4× size cut
  with no visible loss at reading size. These are the command's defaults, overridable
  with `--jpeg-quality` / `--dpi`.

---

## 9. What a guide in this genre contains

From four official PDFs, all by different studios, converging on one skeleton:

> cover + spoiler line → contents → "About this guide" (author, spoiler policy, scope,
> where to report errors) → **a three-bullet contract** → character roster → body →
> thanks

The contract is the useful part, because it doubles as an editorial spec — if a line
isn't one of these three, cut it:

1. Hint the recommended action
2. Show how the character reacts
3. Warn about the consequences

Other findings worth keeping:

- **Publish the hidden numbers.** Every shipping guide exposes raw deltas
  (`RP Chloe +1`). It is the single highest-value thing a guide does that the game does
  not.
- **Ship negative information as a first-class section.** *"If a choice isn't mentioned
  here, it doesn't affect progression"* converts a 255-choice graph into a short list of
  load-bearing decisions.
- **"Spoiler-free" in this genre does not mean staged hints.** It means no plot summary
  — choice-and-consequence only, under a read-at-your-own-risk banner. Graduated hint
  ladders are an adventure-game tradition with no foothold here. If you want tiers, ship
  two products (the genre does Basic vs Advanced), not hint levels in one document.
- **Sandboxes organise per-character**, each rung carrying (location, day-type, time
  window, threshold). Linear openings organise by day then time-of-day.
- **Budget 20–40 pages.** Below ~6 it reads as a manual; above ~70 it stops being read.
- **Version the guide with the build** and regenerate every release.

Writing the guide is also a cheap audit: every warning you have to write — *"this looks
fine but soft-locks you"* — is a place the game should have signalled and didn't.

---

## 10. Verified output

`python manage.py build_guide --game vesper`, run from the committed tree:

- 11 pages, 294 KB
- 17 PDF bookmarks, two levels, resolving to correct pages
- 60 working links on the contents sheet; TOC page numbers spot-checked against reality
- 33 embedded images, cover present
- version stamped `0.1.5`, read from the TOML and not the front matter
- embedded font table: Charter, Menlo, Helvetica Neue — no uncontrolled fallbacks
- no empty pages; no heading stranded at a page foot; every page opens under a running
  header naming its chapter

Page fill runs 92–98% through the front half and 30–48% on the later chapters, because
`h1` forces a page break and those chapters are short. That is a knob, not a defect —
drop the forced break if chapters should flow.

---

## 11. Open items

- **The cheat chapter is a stub.** No game in this repo ships a player-facing cheat
  page yet. `ship-gate.md` §3 specifies it as an authored TOML canvas (money and
  climbing meters only; never a flag, never a `*_stage`/counter trait), but a later
  cheat-mechanism study contests several of those claims. The guide chapter should be
  rewritten against whatever actually ships. Given the demand study — ~73% of ask-weight
  in 2,389 comments is *"what's the code"* — this is likely the highest-value page in
  the document.
- **Docker/CI is uncosted.** The `apt-get` line for `python:3.10-slim` is documented in
  `requirements/base.txt` but is not in the Dockerfile and has not been tested. If this
  ever needs to run in a container, seriously reconsider Typst (§3).
- **Only Vesper and The Inheritance** can render a portrait-bearing guide from a clean
  clone (§6).
- **Multi-column flow (`column-count`) is untested** — WeasyPrint's docs describe only
  "basic support". If a design ever wants magazine columns, test before committing.
- **Platform content policy unchecked.** The deliverable is an explicit adult guide with
  NSFW imagery hosted on Patreon. Nobody has verified it against Patreon's adult-content
  rules or considered whether an alternative host is needed.

---

## 12. Adding a style, or a game

**A new visual treatment:** create `scripts/guide_styles/<name>/` containing
`template.html` and `style.css`, honour the nine slots in §5, then
`--style scripts/guide_styles/<name>`.

**A new game:** create `games/<slug>/guide/guide.md` with the front matter from §6,
point images at tracked media, and run `manage.py build_guide --game <slug>`. The
version stamp and output filename come free.
