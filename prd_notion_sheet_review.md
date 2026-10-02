# PRD — Notion mirror for the sheet review loop

**Status:** proposed, unsigned · **Date:** 2026-09-05 · **Owner:** LO signs, ENI builds
**Governs:** `.claude/skills/author-game-v2/references/the-sheets.md`
**Blocked on:** a Notion parent page URL and an internal integration token

---

## 1. The one line

Mirror every `games/<slug>/sheets/**.md` to a Notion database so LO can read, argue with and sign
sheets from a phone — with **git** as the change detector and **disk** as the source of truth.

## 2. The problem

`the-sheets.md` makes the sheets the review surface: a sandbox in this engine cannot be reviewed by
playing it, so the board phase ends in documents LO reads and signs. The workflow is
`[REVIEW] → LO reads and edits → [READY] → built → [GAME-READY]` (`the-sheets.md:22`).

Three frictions, all ergonomic rather than technical:

1. **Reading 138 markdown files requires the machine the repo is on.** Sign-off is the one step in
   the pipeline that is pure judgement and needs no terminal, and it is the step chained hardest to
   one.
2. **Nothing shows the set.** Status is per-file, in the H1. There is no view answering *"what is in
   REVIEW right now, across every game."*
3. **A change to a signed sheet is silent.** A `[READY]` sheet edited after sign-off keeps its
   marker. Nothing re-opens it, and nothing shows what moved.

## 3. Non-goals — read these before scoring the design

- **This is not a drift checker.** `the-sheets.md:82` costed and dropped a sheet-versus-build row
  diff on 2026-09-03: two incompatible parsers, a fuzzy name join because zero of 43 row cells
  contain an id, and a denominator nobody has defined. That finding stands and this PRD does not
  reverse it. A Notion board makes drift **visible to a human**; it does not detect it.
  `act_quad_row` is still named 3 times in `orientation` sheets and gone from the build, and this
  ships without noticing.
- **It is not a second source of truth.** Disk wins, always. See §8.
- **It does not read or write TOML, canvases, or `gates.py`.** No instrument changes.
- **It does not measure anything.** Every count on a sheet stays on the intent side of the
  measured/intent split (`the-sheets.md` S1).

## 4. What was verified

### 4.1 On disk, 2026-09-05

| | |
|---|---|
| sheets | **138** — `orientation` 27 · `probation` 5 · `vesper_two` 106 |
| words | 55,437 total; largest single sheet 1,856 words (~12 KB) |
| H1 status marker | **138 of 138.** 133 `[READY]`, 5 `[REVIEW]` |
| git-tracked | 133. The 5 untracked are `probation` — exactly the 5 in `[REVIEW]` |
| raw HTML | **6** `<pre>` blocks, all schedule grids (`probation` people ×4, two `OPENING.md`) |

Two of the three blockers named in the `the-sheets.md:82` survey are dead:

- The survey found two incompatible sheet formats. `night_desk` — the fixed-width-ASCII-in-`<pre>`
  game — is gone with the 2026-09-03 `games/` cut. **Every surviving sheet is markdown.**
- The survey needed fuzzy matching to identify a row. This design never parses a row. Its key is the
  **file path**, and its status field is the H1 marker, which is present and well-formed in 138 of
  138 files.

The third blocker — a row label is prose, never an id — is untouched, and is exactly why §3 rules
out row-level work.

### 4.2 Notion, verified against the docs

| capability | verdict |
|---|---|
| markdown in | `POST /v1/pages` with a `markdown` body param |
| markdown out | `GET /v1/pages/:id/markdown` |
| markdown update | `PATCH /v1/pages/:id/markdown`, incl. `old_str`→`new_str` |
| size caps | 500 KB payload · 1000 blocks/request · 2000 chars per rich-text · ~20k blocks/page |
| rate | REST ~3 req/s per connection, 429 carries `Retry-After`. Hosted MCP 180 req/min |
| comments | create on a **page** or a **block** (`parent.block_id`); list open ones |
| comments — cannot | start a new text-anchored inline discussion · read resolved · resolve or reopen |
| page history / diff | **no API.** Side-by-side compare is UI-only; free-plan history is 7 days |
| DB automations | trigger on property edit; webhook action is POST-only and ships **properties only, never page content** |
| outbound webhooks | `page.content_updated`, `comment.created`, `page.locked`, `data_source.schema_updated` |
| auth | REST takes an internal `ntn_` token as `Authorization: Bearer`. Hosted MCP is **OAuth browser login only — non-interactive is not supported** |

Largest sheet is 12 KB against a 500 KB cap. Size is a non-issue.

**The two consequences that shape the design:**

1. A git hook cannot use MCP (no non-interactive auth). The sync is a **REST script**.
2. Notion cannot detect or display a change to a sheet body. Automations see properties only, and
   there is no diff API. **Git detects the change and the script renders the diff.**

Neither is a compromise. `sheets/` is git-tracked, so the diff can be anchored to *the commit the
sheet was signed at* rather than to a wall-clock timestamp — which is strictly better than Notion's
own version compare.

## 5. Architecture

```
disk (authoritative)                       Notion (mirror)

games/*/sheets/**.md  ──[push]──────────►  Sheets DB
      ▲                                    • one row per sheet
      │                                    • page body = the sheet
      │                                    • CHANGES block on top when re-opened
      │
      └───[pull]──────────────────────────  Status · 4 verdict boxes · comments

git post-commit hook ──► push only the sheets this commit touched
```

**Content flows one way. Status and comments flow back.**

The reason is measured, not stylistic: `GET /v1/pages/:id/markdown` does not round-trip our sheets
byte-identically. Callouts, `<pre>`, and the `| | |` header tables normalise. A two-way body sync
would emit a spurious diff on every sheet on every run, forever, which destroys the one signal this
whole thing exists to carry.

So LO argues in **comments**, and ENI applies the comment to disk. That is the code-review loop, and
it preserves the sheet formatting, which is load-bearing — `⚠️` boxes and the `**bold** = a row` /
`├ *italic*` = not a row markers change what a sheet means.

## 6. The database

```
Game Sheets (page)
  └─ Games (database)              one row per game — the list
       └─ <game> (row)
            └─ Sheets (database)   that game's sheets, its own board
```

⚠️ **This reverses the original §6.** It proposed one flat database across all games with a `Game`
column, on the argument that *everything in REVIEW right now* is the view that matters and per-game
databases cannot show it. **LO overruled it on 2026-09-05: games are the list, and each game gets its
own board.**

He is right and the original argument was thin. A 138-row table where 133 rows belong to games that
are not being reviewed is not a review surface, it is a haystack — and the cross-game view survives
anyway as three numbers on the `Games` row (`Sheets` · `In review` · `Ready`), which is the roll-up
actually wanted. The `Game` column is deleted: the board a sheet sits in *is* its game.

**Games** — one row per game, counts refreshed on every full push:

| property | type | notes |
|---|---|---|
| `Name` | title | the game slug |
| `Sheets` | number | how many sheets exist |
| `In review` | number | **the number that decides where to look** |
| `Ready` | number | signed, including `GAME-READY` |
| `Last pushed` | date | |

**Sheets** — one board inside each game row:

| property | type | written by | notes |
|---|---|---|---|
| `Name` | title | push | `probation · person · rae` |
| `Path` | rich text | push | `games/probation/sheets/people/rae.md` — **the join key** |
| `Kind` | select | push | `opening` · `place` · `person` · `scene` · `system` · `decision` · `index` · `guidance` — from the parent directory |
| `Status` | select | push + **pull** | `REVIEW` · `READY` · `GAME-READY` (`the-sheets.md:22`) |
| `Character` | checkbox | pull | the four-part verdict, `the-sheets.md:35` |
| `Coherence` | checkbox | pull | |
| `Correctness` | checkbox | pull | |
| `Convenience` | checkbox | pull | |
| `Gate-required` | checkbox | push (seed) then manual | S6 — a sheet may not defer what a gate requires |
| `Approved at` | rich text | pull | the commit sha this row was last set `READY` on. **The diff anchor** |
| `Words` | number | push | sortable size; not a measurement of anything |
| `Last pushed` | date | push | |

`Status` is a **Select**, not Notion's Status type: Status groups are fixed (To-do / In progress /
Complete) and buy nothing here, while Select writes cleanly from the API.

**Views:** `Board` and `All sheets`, created per game. Grouping is not settable through the API
(§15.1) and is a two-tap change in the UI.

**Join key is `Path`, scoped to the game's own board.** One paginated query per game builds a
`Path → page_id` map in memory. `.notion_sheets.json` caches the per-game ids; losing it costs
nothing, since `ensure_game` adopts an existing row and an existing `Sheets` child database by name. A row whose file is gone from disk is
**archived, never deleted**.

## 7. The script

`scripts/notion_sheets_sync.py` — stdlib + `requests`, no new dependency.

```
init                      create the DB and the three views under the parent page
push  [--game S] [--all]  push sheets; default = only those changed vs Approved at
pull  [--game S]          read Status, the four boxes and comments back
status                    print every disagreement between disk and Notion; write nothing
```

### 7.1 push, per sheet

1. Read the file. Normalise the 6 `<pre>`…`</pre>` blocks to fenced code.
2. Parse `Game` / `Kind` from the path, `Status` from the H1 marker, `Words` from the body.
3. Look up `Path` in the map. Absent → `POST /v1/pages` with `markdown`. Present → continue.
4. If `Approved at` is set and `git diff <sha> -- <path>` is non-empty, build the **CHANGES block**
   (§7.3), set `Status = REVIEW`, and **clear all four verdict checkboxes** — a body change
   invalidates the verdict that was given on the old body.
5. `PATCH /v1/pages/:id/markdown` — replace the whole body with `CHANGES block + sheet`.
6. Update `Words`, `Last pushed`.

**A push never writes a byte to disk.**

### 7.2 pull, per row

1. `Status` differs from the disk H1 → rewrite **only** the H1 marker in place. On a transition into
   `READY`, stamp `Approved at = HEAD` and drop the CHANGES block on the next push.
2. Verdict checkboxes → recorded in the run report; not written into the sheet.
3. `GET /v1/comments?block_id=<page_id>` → print as a work list, newest first, with the page URL.
   `--write-notes` optionally appends a `## REVIEW NOTES` section; **off by default**, because a
   sheet carries labels, gates and consequences, not conversation.

**Known ceiling:** the API cannot read resolved comments and cannot resolve one. A handled comment
therefore keeps reappearing. Mitigation is a gitignored `.notion_handled_comments.json` of ids ENI
has already applied. LO resolving it in the Notion UI also works and is invisible to us — which is
fine, since resolved comments are unreadable either way.

### 7.3 The CHANGES block

Rendered at the very top of the page body:

```
## ⚠ CHANGES SINCE APPROVAL

`a1b2c3d` (approved) → `e4f5g6h` (HEAD) · 3 files ahead

    <fenced diff, unified, path-scoped>
```

A fenced ` ```diff ` code block, **not** a Notion callout — callouts are a supported block type but
the markdown syntax for one is unverified, and a code block is certain. Capped at 1,500 characters
(under the 2000-char rich-text limit) and truncated with
`… N more lines — git diff <sha>..HEAD -- <path>`.

Dropped on the next push after the row transitions to `READY`.

### 7.4 The hook

`scripts/hooks/post-commit`, checked in, symlinked by `dev-setup.sh` (a hook in `.git/hooks/` is not
versioned and would not survive a clone).

```sh
changed=$(git diff-tree --no-commit-id --name-only -r HEAD -- 'games/*/sheets/**')
[ -z "$changed" ] && exit 0
[ -f ~/.config/notion_sheets.env ] || exit 0
( python scripts/notion_sheets_sync.py push --paths $changed >> .notion_sync.log 2>&1 & )
```

Backgrounded, never blocks the commit, silently no-ops when the token is absent so a fresh clone or
CI is unaffected.

### 7.5 Auth and secrets

Token in `~/.config/notion_sheets.env`, **outside the repo**. `.gitignore` already covers `*.log`
(`.gitignore:13`), so it gains one line: `.notion_handled_comments.json`.

⚠️ **`storygen-beep/Story-Gen` is public** (verified 2026-09-02). A token committed here is a token
published. The env file lives outside the working tree for that reason and no code path reads a
token from inside it.

Optional and separate: `makenotion/claude-code-notion-plugin` gives ENI interactive read and comment
access through the hosted MCP server. Useful for the pull-back conversation, unusable by the hook.

## 8. Doctrine change — required, not optional

`the-sheets.md:29` currently reads:

> Status lives **in the document title**, not in a separate tracker.

This PRD builds the separate tracker. The line has to move or the skill is lying about the system it
governs. Proposed replacement:

> Status lives **in the document title**. `scripts/notion_sheets_sync.py` mirrors it to a Notion
> board so a sheet can be read and signed away from the repo — the H1 on disk stays authoritative,
> the mirror never writes content back, and a body change re-opens the row and voids the verdict it
> was given on the old body.

The paragraph's actual argument — that the document is argued over first, and whoever implements it
is not whoever wrote it — is untouched by the mirror and stays as written. A `CHANGELOG.md` bullet
lands in the same turn as the edit.

## 9. Failure modes

| | mitigation |
|---|---|
| token committed to a public repo | env file outside the tree; no in-repo token path exists |
| lossy markdown round-trip | body is one-way; comments carry LO's edits back |
| 429 rate limit | 138 sheets × ~2 requests ≈ 92 s at 3 req/s. Exponential backoff on `Retry-After` |
| disk and Notion disagree on status | `status` prints it and writes nothing. `push` lets disk win, `pull` lets Notion win, and the two never run in one invocation |
| `<pre>` renders as `<unknown>` | normalised to fenced code on push. 6 files |
| sheet deleted on disk | row archived, never deleted — the review history survives the file |
| **sheet drift stays undetected** | out of scope by §3. Named here so it is not mistaken for covered |
| LO edits a body in Notion anyway | `status` reports the row as diverged. The edit is not lost — it is readable via `GET /markdown` — but it is not auto-applied |

## 10. Pilot

**`probation` only — 5 sheets, all `[REVIEW]`, the design currently under review.** Nothing outside
`games/probation/` and `scripts/` is touched. Its 5 sheets are `OPENING.md` plus four people;
`places/` and `scenes/` exist and are empty.

⚠️ **Precondition: `games/probation/` is entirely untracked — 0 files in git.** The diff anchor is a
commit sha, so check 3 below cannot run until probation is committed. First push therefore marks all
5 rows new, with no CHANGES block, and the loop only closes on the commit after that.

Acceptance is six checks, all observable:

1. 5 rows exist; the board grouped by `Status` shows 5 in `REVIEW`.
2. Page bodies render with tables intact, the schedule grids readable, and the `⚠️` lines present.
3. Edit `rae.md`, commit → within 60 s the row carries a CHANGES block naming both shas and the
   changed lines, with the four verdict boxes cleared.
4. Set a row `READY` and tick the four boxes in Notion → `pull` rewrites that sheet's H1 to
   `[READY]` and stamps `Approved at`.
5. Comment on a page in Notion → `pull` prints it with the page URL.
6. `git status` shows **zero** sheet-content changes attributable to a push.

Then the only question that matters, and it is LO's: **does reading probation this way beat reading
the files?** A no stops the project at five pages.

## 11. Rollout, if the pilot holds

1. Backfill `orientation` (27) and `vesper_two` (106). ~92 s.
2. Symlink the hook via `dev-setup.sh`.
3. Rewrite `the-sheets.md:29` per §8, plus the `CHANGELOG.md` bullet in the same turn.
4. `authoring_state.json` untouched — it records what a release did, and review status is not that.

## 12. Cost

~250–300 lines of Python, one hook, one doctrine edit. Half a session for the pilot, plus the 5
minutes of LO's setup in §13.

## 13. What LO supplies

1. A Notion page to parent the DB under — the URL.
2. `notion.so/my-integrations` → new **internal** integration → share that page with it.
3. The `ntn_` token in `~/.config/notion_sheets.env` as `NOTION_TOKEN=…`. Not in the repo, not in
   chat.
4. Optional: `/plugin marketplace add makenotion/claude-code-notion-plugin` and the OAuth login.

## 14. Signed

Four calls, taken as agreed on 2026-09-05 unless struck here:

- pilot is `probation`
- body one-way disk → Notion; LO argues in comments
- disk H1 is authoritative for status
- **one board per game**; `Games` is the list (revised 2026-09-05, replacing the flat database)

`[ ] LO signs`

---

## 15. As built — pilot, 2026-09-05

`scripts/notion_sheets_sync.py` · 440 lines, stdlib only · database
`72766ccb-148b-4fae-8f8c-42c2c98f6de3` under **Game Sheets**, workspace `Aman`, integration
`NutGames`. Five `probation` rows live. Views `Board` · `By game` · `Needs me` created.

### 15.1 Engine facts, each verified against the live API

Six things the docs did not say, or said wrongly. All found by probing, not by reading.

- **`PATCH /v1/pages/{id}/markdown` takes `new_str`, not `markdown`.** The four valid `type` values
  are `insert_content` · `replace_content_range` · `update_content` · `replace_content`. Whole-body
  replace is `{"type":"replace_content","replace_content":{"new_str": md}}`. The guide's only worked
  example is the `old_str`/`new_str` search-replace, which is the wrong tool for a mirror.
- **Trashing is `{"in_trash": true}`.** `{"archived": true}` is rejected outright in `2026-03-11`:
  *"body.archived should be not present"*. Every pre-2026 example on the web uses `archived`.
- **`POST /v1/views` exists** and wants `database_id` **and** `data_source_id` **and** `name` **and**
  `type` at the top level. The type-specific `board: {"group_by": …}` config was rejected; the view
  is created ungrouped and grouping is set in the UI. Not worth more API archaeology.
- **A bare ``` fence gets a guessed language.** Notion typed a schedule grid as `javascript` and
  syntax-coloured it into noise. The normaliser emits ```` ```text ```` explicitly.
- **`POST /v1/search` sorts by last-edited, so `results[0]` is a trap.** `init` took a scratch page
  created two minutes earlier as the parent and built the database under it. It now requires a
  workspace-level page, refuses to guess between two, and takes `--parent`.
- **File-upload ceiling on this workspace is 5 MiB**, not the 20 MiB in the docs
  (`/v1/users/me` → `bot.owner.workspace_limits`). Irrelevant today, relevant if sheets ever carry
  images.

### 15.2 Round-trip fidelity, measured

`games/probation/sheets/people/rae.md` — 3,177 chars out, 3,375 back, **92.6% similarity**, zero
`unknown_block_ids`, not truncated.

Headings, `⚠️` lines, blockquotes, bold, inline code and ```` ```diff ```` blocks all survive.
**Markdown tables render as real Notion tables and read back as HTML `<table>`.** That single
asymmetry is the whole case for §5's one-way body rule, and it is now measured rather than predicted.

### 15.3 The re-open loop, proven

Proven on `orientation/sheets/places/the_quad.md` — a sheet with real history — rather than by
editing a signed sheet: the row was stamped `READY` with all four verdict boxes ticked and
`Approved at` set to the commit before its last change, then re-pushed.

Result: `Status` `READY → REVIEW`, all four boxes cleared, and the page opened with the real 30-line
unified diff under `## ⚠ CHANGES SINCE APPROVAL`, naming `a448772 (approved) → d6f41d0 (HEAD)`. The
test row was then trashed. **No sheet on disk was edited to produce this.**

### 15.4 Still open

1. **`games/probation/` is uncommitted**, so the live loop cannot close on the pilot game itself —
   §10's precondition, awaiting LO's okay to commit.
2. **The hook is not installed.** `scripts/hooks/post-commit` and the `dev-setup.sh` symlink are
   written after the pilot verdict, not before it.
3. **Board grouping** is a two-tap UI step; see 15.1.
4. **Rotate the token.** It was pasted into a session transcript on 2026-09-05. Delete the `NutGames`
   integration and issue a new one once the pilot is judged.

### 15.5 Revision — per-game boards, 2026-09-05

Restructured on LO's call (see §6). Rebuilt and repopulated: **`Games` database
`30f2d73d-ac20-4079-a334-ca6544f45429`**, three rows, one `Sheets` board inside each.

| game | sheets | in review | ready |
|---|---|---|---|
| `orientation` | 27 | 0 | 27 |
| `probation` | 5 | **5** | 0 |
| `vesper_two` | 106 | 0 | 106 |

**138 on disk · 138 in Notion**, no disagreements. The pilot stopped being probation-only here: a
list of one game demonstrates nothing about a list, and with the script working the other 133 sheets
cost two minutes of API calls.

**One more verified engine fact:** a database can be created inside a *database row's* page —
`POST /v1/databases` with `parent.page_id` set to the row id. Probed before the rewrite rather than
assumed, because the whole shape depends on it. `ensure_game` finds an existing one by listing the
row's block children for a `child_database` whose title is `Sheets`.

### 15.6 Review order, 2026-09-05 — derived, not typed

LO asked for `1_` / `2_` / `3_` filename prefixes so review order is visible in Notion and on disk.
The outcome shipped; the mechanism did not, for two measured reasons:

- **43 of 138 sheets already carry a two-digit number, and it means the RUNG** —
  `ray_03_the_offer`, `colm_04_does_not_remember`. A prefix makes `4_ray_03_the_offer.md`: two
  numbers, two meanings, one filename.
- **80 cross-references to `.md` files live across 46 of the 138 sheets.** A rename breaks them and
  orphans every Notion row, since `Path` is the join key.

**Order is a property of the KIND, and `the-sheets.md` already fixes it** — so it is derived:

| # | kind | why here |
|---|---|---|
| 1 | `decision` | everything else is reconciled against it (S6) |
| 2 | `system` | *"written FIRST and the place sheets are written against them"* (SY1–SY3) |
| 3 | `place` | written against the systems |
| 4 | `person` | a place × hours grid, so its places must exist (S5) |
| 5 | `scene` | one rung of a person |
| 6–9 | `opening` · `guidance` · `index` · `format` | need the world they describe |

Shipped with it:

- **`Order`** number property on every board, and the row title now leads with it —
  `3 · place · the_counter`. The game left the title; the board it sits in is the game.
- **`games/<slug>/sheets/REVIEW_ORDER.md`** — the same order as a file, regenerated on every push,
  excluded from the mirror. Reading the order no longer needs a browser.
- **`DECISIONS.md` is now mirrored.** It is one of the six sheet types and carries a status marker,
  but it lives at the game root rather than under `sheets/`, so it had been invisible to the sync —
  a real gap, found by asking what order 1 was. Three rows added, one per game.

If LO still wants literal filename prefixes after this, the rename is a separate job: 80 references
to fix and a `Path`-aware migration so rows are moved rather than orphaned.
