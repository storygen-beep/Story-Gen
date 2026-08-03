# Pull requests, issues, repositories — full surface

Command lists are from `gh <cmd> --help` on gh 2.86.0. Every subcommand here
also accepts `-R/--repo OWNER/REPO` to target a different repository, and most
`list`/`view` commands accept `--json` for scripting (see scripting.md).

## Pull requests (`gh pr`)

| Subcommand | Purpose |
|---|---|
| `create` | Open a PR from the current (or `--head`) branch |
| `list` | List PRs (filter by `--state/--label/--author/--base/--head`) |
| `status` | PRs you authored, are assigned, or are asked to review |
| `view` | Show a PR (`--comments`, `--web`, `--json`) |
| `diff` | Show the diff (`--name-only`, `--color`) |
| `checkout` | Check the PR out locally as a git branch |
| `checks` | CI check status (`--watch`, `--required`) |
| `review` | `--approve` / `--request-changes` / `--comment` |
| `comment` | Add a top-level comment |
| `edit` | Change title/body/labels/reviewers/base after creation |
| `ready` | Flip a draft PR to ready-for-review |
| `merge` | Merge (`--merge`/`--squash`/`--rebase`, `--auto`, `--delete-branch`) |
| `close` / `reopen` | Close / reopen |
| `lock` / `unlock` | Lock or unlock the conversation |
| `revert` | Open a PR that reverts a merged PR |
| `update-branch` | Update the PR branch with the base |

### `gh pr create` — key flags
- `-f, --fill` — title/body from commit info; `--fill-first` (first commit only), `--fill-verbose` (msg+body).
- `-t, --title` / `-b, --body` / `-F, --body-file FILE` (`-` = stdin) / `-T, --template FILE`.
- `-B, --base BRANCH` / `-H, --head BRANCH`.
- `-d, --draft` — open as draft.
- `-r, --reviewer HANDLE` (person or team), `-a, --assignee LOGIN` (`@me` self-assigns).
- `-l, --label`, `-m, --milestone`, `-p, --project`.
- `-w, --web` — finish in the browser; `--dry-run` — print, don't create.

```bash
gh pr create --fill --reviewer LO --label engine
gh pr create -t "Wire energy gate" -F pr-body.md -B main -d
git commit && git push && gh pr create --fill-first --web
```

### `gh pr merge` — key flags
- Strategy (pick one): `-m, --merge`, `-s, --squash`, `-r, --rebase`.
- `--auto` — enable auto-merge (merges when requirements pass); `--disable-auto` to cancel.
- `-d, --delete-branch` — delete local + remote branch after merge.
- `--admin` — merge bypassing unmet requirements (needs admin).
- `-t, --subject` / `-b, --body` / `-F, --body-file` — merge-commit message.
- `--match-head-commit SHA` — only merge if HEAD still matches (guards against races).

```bash
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --rebase --auto
```

### Reviewing
```bash
gh pr checks 123 --watch                 # block until CI resolves; non-zero if not green
gh pr review 123 --approve
gh pr review 123 --request-changes -b "needs tests"
gh pr diff 123 --name-only               # just the changed files
```

## Issues (`gh issue`)

| Subcommand | Purpose |
|---|---|
| `create` | New issue (`--title/--body/--label/--assignee/--milestone/--project`) |
| `list` | List issues (filter by `--label/--state/--assignee/--author/--milestone`) |
| `status` | Issues relevant to you |
| `view` | Show an issue (`--comments`, `--web`, `--json`) |
| `comment` | Add a comment (`-b` / `-F file`) |
| `edit` | Edit title/body/labels/assignees/milestone |
| `close` / `reopen` | `--reason completed` or `not planned` on close |
| `develop` | Create/list a branch linked to the issue (`--checkout`) |
| `transfer` | Move the issue to another repo |
| `pin` / `unpin` | Pin/unpin on the repo's issue list |
| `lock` / `unlock` | Lock/unlock the conversation |
| `delete` | Delete (irreversible; needs admin) |

```bash
gh issue create -t "Stale-save UUID bug" -b "rebuild regenerates NPC UUIDs" -l bug -a @me
gh issue list --label bug --state open --json number,title --jq '.[] | "\(.number) \(.title)"'
gh issue develop 88 --checkout           # branch + checkout, linked to the issue
gh issue close 88 --reason "not planned"
```

## Repositories (`gh repo`)

| Subcommand | Purpose |
|---|---|
| `create` | New repo (interactive, or `--source=. --push`, `--template`, `--clone`) |
| `clone` | Clone `OWNER/REPO` (adds upstream remote for forks) |
| `fork` | Fork (`--clone`, `--remote`) |
| `view` | Show repo / README (`--web`, `--json`) |
| `list` | List repos for a user/org (filters: `--source`, `--fork`, `--language`, `--visibility`) |
| `edit` | Change description, topics, visibility, default branch, features |
| `sync` | Sync a fork (or branch) with upstream |
| `set-default` | Pin which repo `gh` targets in this directory |
| `rename` | Rename the repo |
| `archive` / `unarchive` | Archive / unarchive |
| `delete` | Delete (needs `delete_repo` scope; prompts) |
| `clone`/`fork` aside: | `deploy-key`, `autolink`, `gitignore`, `license`, `gitignore list`, `license list` for templates/metadata |

```bash
gh repo create story-gen --private --source=. --remote=origin --push
gh repo clone github/awesome-copilot
gh repo fork cli/cli --clone
gh repo edit --add-topic interactive-fiction --add-topic sugarcube
gh repo view --json nameWithOwner,defaultBranchRef,isPrivate,diskUsage
gh repo set-default OWNER/REPO            # so -R isn't needed every command
```

### `gh repo create` modes
- **From scratch (interactive):** `gh repo create` and answer prompts.
- **From an existing local dir:** `gh repo create NAME --source=. --push` (creates the
  remote, sets `origin`, pushes).
- **From a template:** `gh repo create NAME --template OWNER/TEMPLATE`.
- **Fork-and-work:** `gh repo fork OWNER/REPO --clone` then branch and `gh pr create`.
