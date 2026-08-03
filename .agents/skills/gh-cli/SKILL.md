---
name: gh-cli
description: >-
  GitHub CLI (`gh`) reference for working with GitHub from the command line.
  Use this whenever a task involves GitHub operations a terminal can do: opening,
  reviewing, or merging pull requests; creating/listing/closing issues; checking
  CI status or downloading Actions artifacts; cloning/forking/creating repos;
  cutting releases; managing gists, projects, codespaces, secrets, variables, or
  labels; or hitting the GitHub REST/GraphQL API via `gh api`. Trigger on
  phrases like "open a PR", "merge this PR", "check the CI", "why did the build
  fail", "create a github issue", "download the workflow artifact", "list my
  repos", "query the github api", "make a release", or any command starting with
  `gh `. Prefer this over raw `git` + web UI or hand-built `curl` calls whenever
  the data lives on GitHub rather than in the local git tree. Verified against
  gh 2.86.0.
---

# GitHub CLI (`gh`)

`gh` is the official command-line client for GitHub. It authenticates once, then
turns GitHub's web surface — PRs, issues, Actions, releases, the API — into
scriptable commands. Reach for it whenever the thing you need lives **on GitHub**
(a PR's review state, a workflow run's logs, an issue list) rather than in the
local git tree, where plain `git` is the right tool.

Why `gh` over the alternatives:
- **Over the web UI**: scriptable, diffable, no context switch, works in CI and agents.
- **Over raw `curl`**: handles auth, pagination, hostnames, and JSON shaping for you.
- **Alongside `git`**: `git` moves commits; `gh` moves the GitHub-side objects
  (PRs, reviews, releases). They complement each other — `gh pr checkout` even
  drives `git` for you.

## Orientation: the command families

Run `gh <command> --help` for any of these — help is authoritative and version-correct.

| Family | Commands | What it's for |
|---|---|---|
| Auth | `gh auth login/status/switch/token/refresh/setup-git` | Sign in, manage accounts/tokens |
| Repos | `gh repo clone/create/fork/view/edit/list/sync/...` | Repository lifecycle |
| Pull requests | `gh pr create/checkout/view/diff/review/merge/checks/...` | The PR workflow |
| Issues | `gh issue create/list/view/edit/close/comment/develop/...` | Issue tracking |
| Actions | `gh run`, `gh workflow`, `gh cache` | CI runs, workflows, caches |
| Releases | `gh release create/upload/download/view/...` | Tagged releases + assets |
| Secrets/Vars | `gh secret`, `gh variable` | Actions/Codespaces config |
| API | `gh api` | Any REST or GraphQL endpoint |
| Search | `gh search repos/issues/prs/code/commits` | Cross-GitHub search |
| More | `gh gist`, `gh project`, `gh codespace`, `gh label`, `gh extension`, `gh alias`, `gh config`, `gh org`, `gh ruleset`, `gh browse`, `gh status`, `gh ssh-key`, `gh gpg-key`, `gh attestation` | Long tail |

Two flags work almost everywhere and are worth burning into memory:
- **`-R, --repo OWNER/REPO`** (or `HOST/OWNER/REPO`) — act on a repo other than
  the current directory's. Lets you run `gh` from anywhere.
- **`--json <fields>` + `--jq` / `--template`** — turn human output into machine
  data. This is the single most important capability for scripting and agents;
  see [references/scripting.md](references/scripting.md).

## When to read the reference files

SKILL.md covers auth, the scripting model, and the three daily workflows (PR /
issue / repo). For anything deeper, load the focused file — don't guess at flags:

- **[references/scripting.md](references/scripting.md)** — `gh api`, `--json`/`--jq`/`--template`, pagination, exit codes, GraphQL, and recipes. Read this whenever you need to *extract or pipe GitHub data*, not just perform an action.
- **[references/workflows.md](references/workflows.md)** — full PR / issue / repo command surface with flags and worked examples.
- **[references/actions.md](references/actions.md)** — `gh run`, `gh workflow`, `gh cache`, `gh secret`, `gh variable`: driving and debugging CI from the terminal.
- **[references/reference.md](references/reference.md)** — releases, gists, projects, codespaces, search, labels, extensions, aliases, config, and the rest, each with its subcommand index.

## Authentication (do this first)

`gh` needs a credential before most commands work. Check before assuming:

```bash
gh auth status              # who am I, on which host, with what scopes
```

Interactive login (opens a browser or device-code flow):

```bash
gh auth login                          # github.com, walks you through it
gh auth login --hostname ghe.acme.com  # GitHub Enterprise Server
gh auth login --scopes "repo,read:org,workflow"   # request extra scopes up front
```

Non-interactive / CI / agents — feed a token on stdin or via env:

```bash
echo "$MY_PAT" | gh auth login --with-token
# or, simplest in automation: just export the token and skip `login` entirely
export GH_TOKEN=ghp_xxx        # github.com
export GH_ENTERPRISE_TOKEN=... # GHE host
```

`gh` reads `GH_TOKEN` (then `GITHUB_TOKEN`) automatically, so in CI you usually
don't run `gh auth login` at all. Other useful env vars:

- `GH_REPO=OWNER/REPO` — default repo for commands run outside a clone.
- `GH_HOST` — default hostname (for Enterprise).
- `GH_EDITOR` / `GH_BROWSER` / `GH_PAGER` — override editor, browser, pager.
- `GH_DEBUG=api` — dump HTTP traffic when debugging.

Multi-account: `gh auth switch` flips the active account; `gh auth token` prints
the current token (handy for piping into other tools). Let git use gh's creds for
push/pull over HTTPS with `gh auth setup-git`.

## Daily workflow: pull requests

The PR loop is the most common reason to reach for `gh`. Core moves:

```bash
# Create a PR from the current branch. --fill reuses commit subject/body as title/body.
gh pr create --fill
gh pr create --title "Fix energy gate" --body "Closes #42" --base main --reviewer LO --label bug

# See what's relevant to you, then open one.
gh pr status               # PRs you authored / are assigned / requested to review
gh pr list --state open --author "@me"
gh pr view 123             # summary in terminal; add --web to open in browser
gh pr view 123 --comments  # include the conversation
gh pr diff 123             # the actual changes

# Check out someone's PR locally to test it (drives git for you).
gh pr checkout 123

# CI / review state.
gh pr checks 123           # CI status per check; --watch to block until done
gh pr review 123 --approve              # or --request-changes / --comment -b "..."

# Merge. Pick the strategy explicitly; --auto merges once checks pass.
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --merge --auto          # queue auto-merge
```

`--fill` (commit info → PR body), `-w/--web` (hand off to browser), and `-R`
(target another repo) recur across these. Full flag list and the issue/repo
surfaces are in [references/workflows.md](references/workflows.md).

## Daily workflow: issues

```bash
gh issue create --title "Schedule page empty after rebuild" --body "Stale-save UUID bug" --label bug
gh issue list --label bug --state open --assignee "@me"
gh issue view 88                  # add --web to open in browser
gh issue comment 88 --body "Repro: rebuild then restart"
gh issue close 88 --reason completed
gh issue develop 88 --checkout    # create + check out a branch linked to the issue
```

## Daily workflow: repositories

```bash
gh repo clone OWNER/REPO              # clone (no need to know the full URL)
gh repo create my-proj --private --source=. --push   # make a repo from the current dir
gh repo fork OWNER/REPO --clone      # fork and clone in one step
gh repo view OWNER/REPO --web        # open in browser
gh repo view OWNER/REPO --json nameWithOwner,defaultBranchRef,stargazerCount
gh repo set-default OWNER/REPO       # pin which repo gh targets in this directory
```

## The habit that makes `gh` powerful

When you want *data*, not a printed table, add `--json` with the fields you need.
Run it once with an empty `--json` to discover the field names, then narrow with
`--jq`:

```bash
gh pr list --json                          # ERROR lists every available field name
gh pr list --json number,title,headRefName --jq '.[] | "\(.number) \(.title)"'
```

This composes with everything and is what to reach for before writing a `gh api`
call or parsing human output with `grep`. The deep dive — including `gh api`,
GraphQL, `--paginate`, and exit-code handling — is in
[references/scripting.md](references/scripting.md).
