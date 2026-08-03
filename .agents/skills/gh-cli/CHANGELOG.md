# Changelog — gh-cli skill

## 2026-06-20 — initial authoring
- Created the skill (`SKILL.md` + `references/scripting.md`, `references/workflows.md`,
  `references/actions.md`, `references/reference.md`).
- **Why:** the obvious pick — `github/awesome-copilot@gh-cli` (official, 21.6K installs) —
  is delisted from the upstream repo (confirmed by full clone: 363 skills, no `gh-cli`),
  so `npx skills add` can't fetch it and skills.sh serves a stale registry entry. No clean
  raw source to reconstruct from either. Authored a fresh, grounded equivalent instead.
- **How verified:** every command family, subcommand, and flag was captured from `gh --help`
  on the locally installed **gh 2.86.0** (commands, `gh pr create/merge` flags, `gh api`
  flags, `gh run view --log-failed/--job`, `gh workflow run --ref/-f/--json`, `gh codespace
  cp -e` + `gh cs` alias, `gh search repos --stars/--language`, `gh label create -c/-d` +
  `clone`, `gh extension` aliases, `gh browse --settings`, `gh alias set --shell`, `gh status
  -e/-o`, `gh config set git_protocol`, env-var list) — not from memory. Frontmatter
  description carries the gh version so staleness is visible later.
