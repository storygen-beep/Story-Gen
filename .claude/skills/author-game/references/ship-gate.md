# ship-gate — the whole-game checklist before a release goes out

**Read this before every release** — the first one and every one after. The pipeline's other audits fire
earlier (Step 6 reviews the *blueprint*, before a word of prose exists), narrower (per beat, per canvas, per
location), or later (`save-safety.md` governs *re*-shipping a game players already hold saves for). Nothing
until now looked at the finished, built game as one thing.

**Not a phase.** `pipeline_phase` ends at `authoring` and stays there — shipping is not the end of a game,
it's an event that recurs (`run-mode.md` "playable ≠ done": a build is *playable, keep iterating*). Vesper
has shipped `releases/v0.1` → `v0.1.3` and is still authoring. Run this gate at each of those moments,
invoked from the milestone build in `beat-authoring.md`.

**Run this before every release — none of it is caught by the build.** Every item below has shipped broken
at least once in this repo while the build was green.

---

## §1 — The meter-ceiling audit (no bar that fills past what it can buy)

**The rule: for every gating trait, `max reachable value` ≤ `its highest authored gate`** — or the top band
says honestly that it's the peak. A meter the player can keep climbing after its last gate is bought reads
as a promise the game doesn't pay. In the 2026-07 top-30 mopoga study the sharpest version of this was a
game whose per-NPC bar could hit its maximum level and still answer "she is not ready" — its players called
the update an insult.

**This is a different test from the three the skill already runs, and it only becomes answerable now:**
- `trait-design.md` "the dead meter" and `step-2-toplevel.md`'s stat-set test ask **does *any* gate read
  this trait** — a ladder gated 10/20/30/40/50 passes even when the value reaches 200.
- `step-6-feedback.md`'s vanishing-HUD lint and `trait-catalog.md` §4 ask **does the value land inside a
  band** — a render question, not a content one.
- The reachable ceiling is only knowable **after authoring**, once every `+N` effect and every throttle
  exist. That's why it lives here.

**⚠️ Reconcile with `trait-catalog.md` §4 before you "fix" anything.** §4 correctly blesses an *unbounded
value* for a one-way climber and tells you to widen the top band so the card still draws. That cures the
**render** symptom — and it can **hide** this one: the sidebar keeps reading "Ruined" forever while nothing
further is purchasable. §4 governs whether the HUD draws; this section governs whether the climb still buys
anything. Both apply.

- [ ] For each gating trait: list its authored thresholds, then its reachable max (every `op=add` on a
      repeatable, times what the throttle allows). Compare.
- [ ] Where reachable overshoots: **cap the terminal add** (`cap = N`), **throttle the tail**, or **author
      an honest terminal band** that names the peak (`step-2-toplevel.md` §6 — "endless ≠ aimless": the
      tracker says you've reached the current edge, never a silent forever-climb).
- [ ] Audit the **source TOML**, not the built HTML — the compiled `trait_effects` JSON is a *preview*:
      value>0-filtered on flat canvases, an unfiltered all-tiers flatten on tiered ones. Never the apply
      path (that's the HTML-escaped `applyAndNotifyTrait` script emitted from raw `effects`). Grep the
      preview and it will show you effects that can't fire *and* hide ones that do.

## §2 — The dangling-promise sweep (every promise is paid, cut, or logged)

Players remember names. In the top-30 study the clearest case was a long-running game whose comment section
was still asking, years later, about a university president the prose had teased and the dev never built. A
named person, place, or act the prose promises is a debt the game has taken on.

Some unpaid promises are **correct** — that's the frontier's job (`step-2-toplevel.md` §6: a *greyed
next-hook seed* is a designed clip-point, and `step-6-feedback.md` requires deferred content to be a
telegraphed locked-visible seed, "counted and logged"). The sweep's question isn't "is anything unpaid" but
**"is every unpaid thing deliberate and on the record."**

- [ ] Extract candidates: read the `paragraph` / `dialog` / `tip` / `locked_text` bodies for proper nouns
      and forward-looking promises ("when the boss gets back", "the man who owns the docks"). A grep by
      capitalised token gets you a candidate list; **it's a scanner, not a verdict** — the same reason
      `prose-truth.md` gives (a promise is spoken in voice, not spelled like a field).
- [ ] For each: **paid** (a canvas exists), **cut** (remove the name), or **logged** — a telegraphed seed
      recorded in the ledger's `feedback.open_gaps`, and narrated forward honestly in-fiction.
- [ ] The Quests page's end-of-content card obeys `quests.md` §7 — no live `(locked)` bullet whose goal
      never flips, no dev-speak leaking into a player `tip`.

## §3 — The cheat page (ship one; the code arrives with the paid guide)

**Ship a player-facing cheat page in the release build.** In the 2026-07 top-30 mopoga study the single
most-liked comment on the large majority of those games was a request for cheat codes — it is the genre's
most universal player behaviour. A game may skip it, but on purpose, like the fail-state declaration.

**How access works (changed 2026-08-23 — read this before copying any older example).**
There is **ONE build**. The same file ships to the portals, to itch and to a supporter. Every row is emitted
live but wrapped in a check on its own unlock flag, so a player who has entered no code sees the page's
title, its intro, a code box and the join line — **no row names, no numbers, no padlocks to count**. Enter a
row's code and that row becomes a button for the rest of the save.

*Why this replaced the free/paid split:* the retired model shipped cheats in a separate downloadable build.
A Patreon exit survey said it plainly — *"I thought cheats would be available for website version I can't
use it on my [phone]"*. A supporter playing on mopoga or gamcore had no route to the thing they paid for,
and the download was 242 MB against a paid delta of 2,630 bytes. Measured against the corpus: **8 of the 26
top mopoga games carry a live supporter-code box inside the free web build; only 3 ship a separate paid
file.** We were in the minority, running its worst version — advertising a lock with no key on the page.

**Corrections to what this section used to claim, both from the 2026-07-26 mechanism study of 26 built
games** (`cheat_page_study.md`):
- *"The #1 game ships a free, default-on cheat menu"* → **free DOOR, paid ROOM.** Apocalyptic World hides
  31 of its 50 rungs behind `recall($suppCode)`. **0 of 12 dissected games ship a fully-free default-on menu.**
- *"The games that sell the codes convert their friction into resentment"* → **unsupported.** A mechanism
  corpus carries no sentiment. What it does show is paywall *instability*: 3 observed retreats, 0 advances.
- *"Re-skin it diegetically"* → **skin the CONTAINER, never the rows.** 0 of 12 write diegetic row labels;
  the menu's second job is economy legibility and fiction destroys it.

**Author it under `[ui.cheat_page]`** — the engine feature, not a canvas. Do **not** copy
`6_dev_shortcuts.toml`; that shape predates the feature. Each `[[ui.cheat_page.grants]]` row needs an
explicit **`id`** (lowercase slug): it is the unlock flag stored in the player's save *and* the key its code
is looked up by, so it must not be derived from a label someone may rename. The page also needs a
**`join_note`** and a **`join_url`** — for a player with no code that line is the only thing on the page
telling them what the box is for, and it is the only advertising the game does.

**Codes never live in the TOML.** That file is committed and this repo is public. They live in
**`games/<slug>/guide/codes.toml`**, untracked (`games/*/guide/` is gitignored), read by
`package_from_toml --codes` (hashes only reach the build) and by `manage.py build_guide` (which prints them
into the paid guide). One source, so the guide cannot document a code the build rejects.
`_assert_no_plaintext_codes()` fails the build if a code word appears anywhere in the output — the likeliest
leak is pasting one into a row's `hint`.

**Pre-screen the words before you build.** That check normalises the *whole output* the same way it
normalises a code — whitespace stripped, upper-cased — so it is not only hints that collide: **any two-word
phrase anywhere in the prose becomes a candidate.** Vesper 0.2.0 picked `GREYCOAT` for the man in the grey
coat and `COLDSTART` for the charge row, and the build rejected both, because the scenes describing them say
"grey coat" and "cold start". Screen the candidate list first — it is one command and it beats a failed
package:

```bash
venv/bin/python - <<'EOF'
import pathlib
hay = "".join(pathlib.Path('games/<slug>/toml_phases/7_final_game.toml').read_text().split()).upper()
for w in ['WORDONE', 'WORDTWO']:          # the candidate words
    print(('LEAK ' if w in hay else 'clean'), w)
EOF
```

Words drawn from the game's own imagery are the ones most likely to fail, which is the trap: they are also
the ones most tempting to pick.

**Codes are scoped to a release.** The hash is salted with `[project] version` and the row id, so last
release's codes stop working by construction and a code cannot open a row it was not issued for. Rotate
per release: new words, new PDF. Do **not** invent a separate rotation mechanism — Apocalyptic World's
version-stamped `$suppCode = 'Patreon0.83'` is the churn machine behind the demand study's finding that
**29% of code-asks are "my old code died"**, because theirs invalidates on a build the player is still on.
Ours does not: codes are baked per build, so a stale portal copy keeps working with the guide beside it.

**Use words, not strings.** They get retyped off a PDF on a phone, where `O`/`0` and `I`/`1` are a coin
flip. Entry strips whitespace and case, so `alphaword`, `ALPHAWORD` and `alpha word` are one code.

**What a row may grant — monotonic, non-exclusive, non-causal state only:**
- ✅ **money**, and the declared climbing meters (`corruption` · `exhibitionism` · `arousal` · `energy` and
      their kin). Give each banded meter the `cap` its top band expects; **money takes no cap** — it's the
      one unbounded countable (`trait-catalog.md` §4) and needs `clamp = false`, or the engine's hardcoded
      0-100 clamp silently caps a wallet at 100.
- ✅ **step in band-sized increments.** Exclusive bands (`gte X` + `lt Y`) are the real stranders: a meter
      SET to max skips every band-entry canvas. Vesper's Renner row moves 10 at a time because his gates sit
      at 10/20/30/40/50.
- ⚠️ **an `lt`-only gate is a WINDOW, not a floor.** Raising a trait past it DELETES the alternative route.
      Vesper's burned yard gates every non-stealth route on `stealth lt N`, which is why its Stealth row caps
      at **9** — one below the first guard threshold. Enumerate a trait's `lt` gates before choosing a cap;
      counting only `gte` gates is how rev 1 of that page missed 19 blocks.
- ❌ **never a story flag.** Flags carry causality, and the flag-chain validator does **not** protect you
      here — it only checks trigger/choice `is_true` gates, and explicitly exempts `is_false` guards,
      `[group]` conditions, quest `when`, and every trait condition. Granting one strands content three
      proven ways: an `is_false` one-shot guard can never match again — which drops the card through the
      same fall-through `quests.md` §6 documents, reaching the permanent blank sidebar by a route §6
      doesn't cover (§6's case is a met goal with no next rung; this is a `when` nothing can satisfy);
      a terminal flag retires standing surfaces and can zone-seal a whole
      location tree before its beat ever plays (`beat-authoring.md`, "retire the standing surface"); and a
      flag stamps `set_day`, re-basing every `days_since_flag` window off a beat that never happened.
- ❌ **never a stage / counter trait** — `<slug>_stage`, `awareness`, and the loop counters
      (`drains_done`, `sex_stage`) are causal traits wearing a number, and they strand identically:
      exclusive bands and first-time clauses (`X lt 1`) skip forever once jumped.

**Rows navigate to themselves.** The at-cap guard is evaluated at RENDER, so only a re-render can grey a row
the instant it caps — and writing state does not re-run gates on the passage you are standing on
(`dev-console-jump.md`). A grant that doesn't navigate looks broken.

**The hint is the guide's material.** Write it as what the number ACTUALLY buys, not what it implies —
Vesper's Bastien hint says the promotions still have to be met on the floor in the bought face, because
relation alone opens nothing. `build_guide` prints these hints straight into the paid guide's code chapter.

**Reference implementation:** `games/vesper/toml_phases/0_systems_spec.toml` ("The Ledger", 6 rows).

**The paper half of this feature lives in `references/player-guide.md`** — the codes file, the chapter skeleton, the rotation rule and the verification gate. A cheat page without a guide to carry its codes is a box nothing opens.

**Don't confuse it with a DEV-SHORTCUT canvas** (`games/vesper/toml_phases/6_dev_shortcuts.toml`) — a
different thing the engine treats differently:
- A canvas whose trigger requires flag **`dev_mode_enabled is_true`** is recognised as a dev shortcut: the
  flag-chain validator, the hint index, and the flag-setter index all **skip** it, and the sidebar renders a
  `<<devJumps>>` link to its entry node.
- `dev_mode_enabled` is set at `StoryInit` **only in `--dev` builds**, so these canvases are inert in a
  release — which is why they may grant flags freely: they fire *into* a specific node, not into open play.
- Invariant, learned the hard way (`games/late_shifts/toml_phases/6_dev_shortcuts.toml` header — the dev
  shortcuts were removed for a clean player build and two dev-only flags had to be cleaned up after them):
  **a dev-only flag must never be REQUIRED by a shipping canvas.** Note the inversion — a *shipping* cheat
  page is a real setter the validator will count, so anything it touches becomes part of the flag chain.
  One more reason it touches no flags.

## §4 — The build gate (what actually goes in the file)

The publish command and its traps are owned by `media.md` §3 "QA build vs publish build" — this is the
gate, not a second copy of the doctrine.

- [ ] Built with **no `--dev` and no `--debug`**, keeping `--video-folder`. `--debug` bakes
      `[IMAGE MISSING]` / `[VIDEO MISSING]` **text into the HTML at build time** — it does not re-check, so
      a debug build ships those placeholders even after the media lands. *(This shipped live once: 147
      baked placeholders in a public Vesper build.)*
- [ ] `grep -c 'IMAGE MISSING\|VIDEO MISSING'` on the built `index.html` == **0**.
- [ ] **Media actually DEPLOYS, not just sits on disk** — every media path the built `index.html` references
      resolves to a **git-tracked** file. Gitignored media (a build whose `videos/` isn't whitelisted) plays
      fine from `file://` and **404s on Pages**; the gap is invisible in any local check. Run per built dir:
      ```bash
      d=games/<slug>/output               # the only build there is since 2026-08-23
      for p in $(grep -oE '\./videos/[A-Za-z0-9_./-]+\.(jpg|jpeg|png|webp|gif|webm|mp4)' "$d/index.html" | sort -u); do
        f="$d/${p#./}"; git ls-files --error-unmatch "$f" >/dev/null 2>&1 || echo "NOT TRACKED -> 404 live: $f"
      done
      ```
      Zero output = every clip ships. *(This shipped live once, on the now-retired paid build: its
      `output-paid/videos/` was gitignored, so media 404'd on Pages though every file sat on disk. The
      two-build split is gone, but the lesson is not — whitelist a build's media in `.gitignore` or it
      404s live, and run this against the path the HTML actually references.)*
- [ ] No dev surface leaked — no `<<devJumps>>` links, no canvas-review or full-map affordance, no
      `[DEV]`-labelled choice.
- [ ] Media type matches the bytes: a block declared `type = "video"` whose file on disk is a `.jpg` is a
      silent mis-ship (`media.md` §2 — the bytes win). Nothing checks this; look.
- [ ] Coverage was actually reviewed — build `--debug` **once, separately**, walk the Missing-Media page,
      then rebuild clean to ship. In a player build the gaps are invisible by design.
- [ ] **No performer named in prose** — grep the merged TOML; the game outlives any performer's
      availability (`media.md` §7b). *(The other two insurance habits — mirroring the media folder and the
      find-media manifest off-tree — are off-repo state this gate can't witness; confirm them by hand at
      the same time.)*

## §5 — Re-run the whole-game scanners

Everything here already exists; the only new instruction is **run them once more against the finished
game**, not just the beat you last touched.

- [ ] `python .claude/skills/author-game/scripts/check_render_buckets.py games/<slug>/toml_phases/7_final_game.toml`
      — every hit triaged (it can't see a hub authored with neither `npc` nor `requires_npc`; verify those
      by reading).
- [ ] `python .claude/skills/author-game/scripts/check_cascade_order.py games/<slug>/toml_phases/7_final_game.toml`
      — exit 0 (it doesn't recurse into `group` blocks; check those by eye).
- [ ] `prose-truth.md` §4's coupled-field detector across the **whole release range**
      (`git diff <last-release>..HEAD`), not one beat — the prose that quoted a moved field is what went
      stale.
- [ ] `rts-flat-prose.md` §7 checks **3** (the narration:dialogue ratio, report the number) and **7** (the
      arousal read-audit) at whole-game scope.
- [ ] `rts-flat-prose.md` §7 check **8** — the counters for Rules 11–14:
      `python3 .claude/skills/author-game-v2/scripts/gates.py <slug>`. **Report the six numbers**
      (`prose texture` · `the sentence explains itself` · `what did not happen` ·
      `history on a repeatable screen` · `the words the player has to already own` · `the act nodes`)
      and clear each bar, or log why not. Ignore every structural gate it fails — those judge a v2 world
      model this skill does not build (§7 check 8 says which lines to read).
      ⚠️ **This is the check that a shipped release failed in front of players.** vesper 0.2.0 passed
      everything above it and still read, in two players' words, like *"an underpowered AI whose mother
      language isn't english."*
- [ ] `location-design.md` §6 — the room-content floor, re-run against the finished map: no reachable room
      with neither plot nor ambient life.

## §6 — Release discipline

- [ ] **Re-shipping?** `save-safety.md` §6 first — diff the merged TOML against the last shipped one and
      confirm no join key moved (ids, live flag/trait keys, stat ranges and tier thresholds, the title). A
      rename is a major version with an announced save reset, never a silent update.
- [ ] Cut the artifact: keep the built HTML as `games/<slug>/releases/v<X.Y[.Z]>.html` so every shipped
      build stays reproducible and diffable (Vesper's convention — `v0.1` through `v0.1.3`; keep whatever
      granularity the game started with, and don't skip a release).
- [ ] Set `[project] version` + `release_date` if the game surfaces the sidebar footer, and bump
      `book_revision` + log the release in `authoring_state.json`'s `decisions_log`.
- [ ] **Check the funding link points where you think it does.** `[project] support_url` /
      `studio_name` are engine defaults unless the game sets them (`engine-reference.md` §8), and the
      link ships at **three** sites — sidebar button plus both intro/age-gate links. This matters most
      off-portal: sites that re-host the free build strip page-level credit but copy the file verbatim,
      so the in-build link is often the only funnel that survives. Grep the built HTML for the host and
      confirm the count is 3.
- [ ] **Paid tier? The guide ships WITH the build, not after it.** New release means new codes and a new
      PDF — the codes are salted with `[project] version`, so last release's guide stops working the moment
      you bump it. A supporter holding a stale guide reads *"No match. This build is vX.Y.Z"* and concludes
      the codes are broken.
      1. Rotate the words in `games/<slug>/guide/codes.toml` and bump its `version` to match.
         Pre-screen them against the merged TOML first (see the plaintext-leak note above).
      2. Re-merge for release with `scripts/merge_toml_phases.py games/<slug> --no-dev`, which drops
         `6_dev_shortcuts.toml`. Dev canvases never *fire* in a non-`--dev` build — their trigger wants a flag
         only `--dev` sets — but they are still emitted as passages and their **labels ride in the shipped
         metadata blob**. Vesper 0.2.0 shipped a build with no dev mode at all that still carried the string
         `"0.1.9: the 0.1.8 end-state"` off a jump label. Omitting `--dev` is not the same as excluding them.
      3. Rebuild with `--codes games/<slug>/guide/codes.toml` (the build **fails** without it, by design).
      3. `python manage.py build_guide --game <slug> --html /tmp/guide.html`
      4. **Run the number gate — it blocks the release:**
         ```bash
         python .claude/skills/author-game/scripts/check_guide_numbers.py \
           games/<slug>/toml_phases/7_final_game.toml games/<slug>/guide/guide.md
         ```
      5. Work `player-guide.md` §7 — markers substituted, every code in the PDF and **no** code in the
         built `index.html`, no colour emoji, no scaffold text, no in-game "Support Us" CTA, schedules
         match `[[npcs.schedules]]`.
- [ ] **Nothing under `games/<slug>/guide/` is ever committed** — not the PDF, not the markdown, above all
      not `codes.toml`. This repo is PUBLIC and serves the Pages portal, so a committed code is a published
      code and a committed guide is a free one. `.gitignore` carries `games/*/guide/`; confirm
      `git status --porcelain games/<slug>/guide` is empty before you push.
- [ ] The ledger's `_active_beat` names what ships next, so the following session opens with the frontier
      in hand rather than re-deriving it.

---

## Cross-references
`references/player-guide.md` (owns the paid guide: codes file, chapters, the number gate) · `references/media.md` §3 (owns the publish command + the `--debug` bake trap) · `references/save-safety.md`
(owns re-ship immutability) · `references/prose-truth.md` (owns the coupled-field detector) ·
`references/location-design.md` §6 (owns the map audit) · `references/quests.md` §6/§7 (the blank-row trap,
the end-of-content card) · `references/trait-catalog.md` §4 (owns clamping and the banded-stat vanish — §1
here extends it) · `references/beat-authoring.md` (the two lint scripts; the milestone build that invokes
this gate) · `references/dev-console-jump.md` (the out-of-band console technique — a different tool from
both the cheat page and dev-shortcut canvases) · `references/run-mode.md` ("playable ≠ done" — shipping is
an event, not an ending).
