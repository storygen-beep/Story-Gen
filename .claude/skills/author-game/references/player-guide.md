# The player guide (the paid PDF)

**What this owns:** the guide a supporter actually buys — what goes in it, how it is built,
how the cheat codes reach it, and the verification that has to pass before it goes out.

**Read this when:** a game is going to have a paid tier, or a release is being cut for a game
that already has one. The cheat *page* (the in-game surface) is owned by `ship-gate.md` §3;
this file owns everything on the paper side and the seam between them.

---

## 1. What the guide is for

**The guide is the paid product.** Not the build. This is the thing that changed on
2026-08-23, and it changed because of one line in a Patreon exit survey:

> *"I thought cheats would be available for website version I can't use it on my [phone]"*

The retired model sold a separate downloadable build carrying the live cheat rows. Measured
on Vesper 0.1.8 before anything was changed: that build was a **2,630-byte** delta over the
free one (357 passages both; only `CheatPage` and `TimeWidgets` differed) shipped as a
**242 MB** zip. Most players meet these games on a portal — mopoga, gamcore — in a browser
tab, often on a phone. A download is not deliverable there. The supporter had paid and had
no route to the thing they bought.

So: **one build ships everywhere, and the paid tier is a PDF.** The PDF carries the cheat
codes and the walkthrough. It is ~300 KB, it opens on anything, and it sits beside the game
tab instead of replacing it.

**What a guide has to carry to be worth money.** A well-made game already ships guidance —
`quests.md` requires it. So the guide cannot just be the quest cards on paper. What it adds:

1. **The whole route at once, in order**, including everything the player's current state has
   not unlocked. In-game they only ever see the cards their state satisfies.
2. **The traps.** Nothing in-game warns that a meter can climb past a window (§6).
3. **Every threshold for one person in one place.** The in-game card shows only the rung the
   player is standing on.
4. **The codes.**

If a guide does not carry all four, it is a reprint and the player will say so.

---

## 2. The pipeline

    python manage.py build_guide --game <slug>

- Source: `games/<slug>/guide/guide.md` — markdown with `Key: value` front matter.
- Style: `scripts/guide_styles/dossier/` (`template.html` + `style.css`).
- Output: `games/<slug>/guide/<slug>_guide_v<version>.pdf`.
- `--html <path>` also writes the intermediate HTML. **Use it** — every check in §7 runs
  against the HTML, not the PDF.

The version stamp is read from the game's merged TOML (`[project] version` / `release_date`),
never from the guide's front matter, so a guide cannot claim a build it was not written for.

Markdown extensions available: `meta`, `tables`, `attr_list`, `admonition` (`!!! warning` /
`!!! spoiler`), `toc` (page numbers come from CSS `target-counter`), `sane_lists`, `smarty`.

### The two generated blocks

Two markers are substituted into the **markdown**, before conversion, so they get real
headings and land in the table of contents:

| Marker | Becomes | Source |
|---|---|---|
| `{{codes}}` | the cheat-code table | `games/<slug>/guide/codes.toml` + the game's `[[ui.cheat_page.grants]]` |
| `{{roster}}` | who is where, and when | `[[npcs.schedules]]` |

**Only these two are generated. Everything else is written.** That split is deliberate and it
is the rule: generate exactly the two things a reader is *actively misled by* when they go
stale — a code that does not work, and a person who is not where the book says. Everything
else is prose, and prose that is a little out of date is survivable.

`{{codes}}` with no `codes.toml` is a hard error. `{{roster}}` with no merged TOML is a hard
error. Neither degrades quietly.

---

## 3. `codes.toml`

```toml
version = "0.1.9"          # must match [project] version, or both tools refuse

[codes]
coin     = "ALPHAWORD"      # keys are [[ui.cheat_page.grants]] ids
fighting = "BETAWORD"
```

**It is untracked, and that is load-bearing.** `games/*/guide/` is gitignored because this
repo is PUBLIC and serves the Pages portal. A code in a committed file is a published code.
The packager bakes only salted hashes; `_assert_no_plaintext_codes()` fails the build if a
code word appears anywhere in the output.

⚠️ **The guide's markdown is untracked too, for the same reason** — it *is* the product. It
therefore has **no version history**; back it up off the repo. (Vesper's original `guide.md`
was committed before this rule and is in public history permanently. It was a layout sample,
so nothing was lost — but the lesson is that this rule is one commit away from being undone.)

**Words, not strings.** They get retyped off a PDF on a phone, where `O`/`0` and `I`/`1` are
a coin flip. A word has no ambiguous characters and survives a typo you can see. Entry strips
whitespace and folds case, so `alphaword`, `ALPHAWORD` and `alpha word` are one code.

⚠️ **Never use a real code as an example — not in this skill, not in a test fixture, not in a
commit message.** Anything written into a tracked file is published the moment it is pushed, and
git history keeps it after you delete it. This was caught at the push gate on 2026-08-23, with
Vesper's six live words sitting in `test_cheat_page.py` and in this file's own example block.
Placeholder words here (`ALPHAWORD`, `BETAWORD`, …) are deliberately unusable as real codes.

**Rotate per release: new words, new PDF.** The hash is salted with `[project] version` and
the row id, so last release's codes stop working by construction and a code cannot open a row
it was not issued for. Do **not** build a second rotation mechanism on top of that.

---

## 4. The chapter skeleton

Eight chapters. This order is not arbitrary — each position was argued for.

1. **Your codes** — `{{codes}}` plus the rules (one per cheat, type once, scoped to this
   release, spaces and case ignored) and a `!!! warning` on what codes will *not* do (move
   meters, never set flags or skip scenes).
   **First, not last.** Genre convention buries cheats at the back; four official walkthrough
   PDFs studied all do. Break it on purpose: this is what the reader opened the file for.
2. **About this guide** — the spoiler line, and the three-bullet contract: where to be · what
   it needs · what it costs you. Plus the two refusals: *it does not retell the story* (the
   prose is what they paid for) and *if a choice is not in here, it does not affect
   progression*.
3. **How the character works** — the meters, their bands as the sidebar shows them, and the
   two or three **facts that explain the economy**. Name them as facts, not as a paragraph.
   Vesper's are: work drains her / sex charges her; coin is not money; the drain is a worn
   weapon that only fires on one finish.
4. **Where everyone is** — `{{roster}}`, plus any hand-written note about surfaces the player
   cannot guess (Vesper: *Sol and Colm are portraits you click inside the room, not location
   cards*).
5. **What to wear** — only if the game gates on clothing. Cover is a re-checked worn garment,
   so right numbers plus wrong clothes equals nothing happening, and the game never says why.
6. **The routes** — the bulk. §5 below.
7. **What will lock you out** — §6. The most valuable chapter and the one most guides skip.
8. **What's in this build** — what exists. **Nothing about the next release** — a teaser here
   reads as an ask, and they already paid.

---

## 5. The routes chapter

**Structure it as the spine in acts, with each NPC's ladder written where the spine reaches
them.** Not "one chapter per NPC" — that loses the order the player actually plays in, and
it forces the reader to reconstruct the spine themselves.

Per act: a short introduction saying what the act is really about and what it costs, then the
rungs. **Per rung, four things and nothing else: where · when · what it needs · what it
opens.** A table is usually right.

Each NPC section ends with a one-line **numbers table** — every threshold that person has.
This is the single highest-value block in the guide, because it is the one thing the in-game
card structurally cannot give you.

### The quest cards are the source

A game that follows `quests.md` already contains its own walkthrough. Each `[[quest_cards]]`
entry carries `text` (what and why), `tip` (exactly what to do), `when` (the state that shows
it) and `goals` (the exact numeric target). Vesper has 61 of them.

**Read them all before writing a line.** They give you the rungs, the order, and every number.
Dump them with the `when`/`goals` conditions resolved and write from that.

**Ordering:** use the authored TOML order. Do **not** build a flag-chain solver — the spine
is a DAG with parallel threads (Vesper's yard thread runs alongside the Renner thread), so a
solver imposes a false linear order. The authored order already reads as story order, because
that is how it was written.

⚠️ **Two things the cards will not give you, and you must add:**

- **Parallel threads.** A card describes its own thread. It cannot tell the reader that two
  threads run at once. Vesper's Act 1 is Renner *and* the burned yard simultaneously, and
  that is the first thing that trips people.
- **Traps buried as asides.** The dangerous facts hide mid-`tip` in a subordinate clause —
  *"keep the cot paid or he won't be"*, *"the stall stays shut to you until you have told him
  what the last one did"*. In play these look exactly like bugs. **Promote every one of them
  to a named trap in chapter 7.**

### What "written fresh" means

Fresh prose means **new connective writing** — where to be, what it needs, what it costs,
what runs alongside what. It does **not** mean new fiction. The guide still never retells a
scene: the writing is the thing they paid for, and describing it here makes it worse and the
document longer.

Reprinting the card `tip` strings verbatim is the failure mode at the other end. The reader
has seen those in-game.

---

## 6. Chapter 7 — what locks you out

Every mechanic that can permanently cost a player content, named, with its real numbers.
Derive these from the build, not from memory:

- **`lt`-only gates are WINDOWS.** Raising the trait past one DELETES the alternative route.
  Enumerate a trait's `lt` gates before you write about it. Vesper's Stealth carries **13**
  `lt` gates against 7 `gte` — climb past them and the fights, the escapes and a Tier-5 scene
  stop being offered, in a save that looks fine.
- **Exclusive bands.** A meter SET to max skips every band-entry scene between here and there.
  This is why cheat rows step in band-sized increments (`ship-gate.md` §3).
- **One-way mechanics.** Vesper: every drain fires only on the anal finish, skin on skin,
  weapon worn and charged. Any other finish spends the evening for nothing.
- **Time-boxed arrangements.** Vesper: Rue's Sunday booking is one night, asked before 20:00,
  served at 20:00 — and *sleeping between arranging and serving rolls the day and lapses it*.
- **Upkeep that silently stalls an act.** Vesper: an unpaid cot stops Act 5 dead, and nothing
  announces it.

---

## 7. Verification — the gate that has to pass

**A wrong number in a paid guide is the one defect a customer discovers for you.** Prose can
be a little loose. A threshold cannot.

**Run the number check. It is a script, not a habit:**

    python .claude/skills/author-game/scripts/check_guide_numbers.py \
        games/<slug>/toml_phases/7_final_game.toml \
        games/<slug>/guide/guide.md

It pulls every `trait op value` condition out of the build (257 of them on Vesper 0.1.9) and
asserts that each threshold the guide asserts exists as a real gate. Exit non-zero blocks the
release.

Then the rest, all against the `--html` output:

- [ ] **Both markers substituted** — no literal `{{` survives.
- [ ] **Every code appears in the guide, and NO code appears in the built `index.html`.**
      Fold whitespace and case on both sides before comparing; a code that survives
      normalisation is still a working code.
- [ ] **No colour emoji.** WeasyPrint renders them undersized and off the baseline —
      measured, not assumed. Text arrows (U+2192) are fine; the pictographic blocks are not.
      Check `0x1F300–0x1FAFF`, `0x2600–0x27BF`, `0xFE00–0xFE0F`, `0x1F000–0x1F2FF`.
- [ ] **No scaffold text** — "to be written", "placeholder", "sample build". A shipped guide
      with a TODO in it is worse than a shorter guide.
- [ ] **No in-game CTA.** Quest-card tips often end with *"Support Us in the sidebar"*. That
      line is correct in the game and insulting in the paid guide. Strip it.
- [ ] **Schedule claims match `[[npcs.schedules]]`** — every time and weekday you wrote.
- [ ] **Page count is what you think.** `mdls -name kMDItemNumberOfPages <pdf>` on macOS;
      counting `/Type /Page` in the raw bytes does NOT work (WeasyPrint compresses the object
      streams and the count comes back 0).
- [ ] **Read it end to end**, against the eight-chapter contract.

### macOS build gotchas (measured 2026-07-26, still current)

- WeasyPrint needs `os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")`
  **inside Python, before the import**. SIP strips `DYLD_*` across an exec of a system binary,
  so exporting it in a wrapper script silently does nothing.
- **WebP explodes ~8–11×** inside a PDF (no WebP filter exists). Convert to JPEG first.
  `write_pdf(optimize_images=True, jpeg_quality=80, dpi=150)` measured a 4× cut.

---

## 8. What to accept, and stop engineering against

- **The guide will leak.** 300 KB versus a 242 MB build; one patron posts it and the codes and
  the walkthrough are public. Of 26 top mopoga games studied, **none watermark**, and patron
  cheat codes are reposted within a version cycle. Rotation is what keeps the product alive,
  not secrecy. Do not build anti-piracy.
- **The codes are crackable.** They live in a public HTML file. So does everyone else's — zero
  of the 26 validate server-side.
- **The game must stay finishable without the guide.** Locked things say what they need; quest
  cards say where to go. Lost players quit — they do not upgrade. Selling the map to people who
  already closed the tab is not a funnel. Guidance in-game is `quests.md`'s job and paywalling
  it undoes the guide's own market.
