# The long tail: releases, gists, projects, codespaces, search, and the rest

Command indexes from `gh <cmd> --help` (gh 2.86.0). All accept `-R/--repo` where
a repo is relevant. When in doubt, `gh <cmd> <sub> --help` is authoritative.

## Releases (`gh release`)

| Subcommand | Purpose |
|---|---|
| `create` | Cut a release for a tag (creates the tag if missing) |
| `list` | List releases |
| `view` | Show a release |
| `edit` | Edit an existing release |
| `delete` | Delete a release; `delete-asset` removes one asset |
| `upload` | Add asset files to a release |
| `download` | Download release assets (`-p PATTERN`, `-D DIR`) |
| `verify` / `verify-asset` | Verify release/asset attestations |

```bash
# Create a release, auto-generating notes, attaching built binaries
gh release create v1.2.0 ./dist/* --generate-notes --title "v1.2.0"
gh release create v1.3.0 --draft --notes-file CHANGELOG.md --target main
gh release upload v1.2.0 ./extra-asset.zip
gh release download v1.2.0 -p "*.tar.gz" -D ./downloads
```

Useful `create` flags: `--generate-notes` (auto notes via GitHub), `-n/--notes`
or `-F/--notes-file -` (stdin), `-d/--draft`, `-p/--prerelease`,
`--target BRANCH_OR_SHA`, `--latest` / `--latest=false`, `--verify-tag` (refuse
if the git tag doesn't exist remotely).

## Gists (`gh gist`)

`create`, `list`, `view`, `edit`, `clone`, `rename`, `delete`.

```bash
gh gist create snippet.py --public --desc "energy gate helper"
echo "scratch note" | gh gist create -        # from stdin
gh gist list
gh gist view <id> --files
```

## Projects (`gh project`) — GitHub Projects (v2)

Owner-scoped (`--owner USER_OR_ORG`). Common: `list`, `view`, `create`, `edit`,
`close`, `copy`, `delete`, plus item and field management:
- Items: `item-list`, `item-add` (add an existing issue/PR by URL), `item-create`
  (draft issue), `item-edit`, `item-archive`, `item-delete`.
- Fields: `field-list`, `field-create`, `field-delete`.
- `link` / `unlink` a project to a repo or team; `mark-template`.

```bash
gh project list --owner LO
gh project item-add 7 --owner LO --url https://github.com/LO/story-gen/issues/88
gh project item-create 7 --owner LO --title "Lane 3 dispatcher polish"
```

Project automation often needs GraphQL via `gh api graphql` — see scripting.md.

## Codespaces (`gh codespace`, alias `gh cs`)

`create`, `list`, `delete`, `stop`, `edit`, `rebuild`, `view`, plus connect/IO:
`ssh`, `code` (open in VS Code), `cp` (copy files local↔remote), `ports`,
`logs`, `jupyter`.

```bash
gh codespace create -R OWNER/REPO -b main
gh codespace list
gh codespace ssh                 # pick interactively, or -c NAME
gh codespace cp -e ./local.txt remote:/workspaces/repo/   # -e expands names
gh codespace ports               # list forwarded ports
gh codespace stop
```

## Search (`gh search`)

`repos`, `issues`, `prs`, `code`, `commits`. Accepts GitHub search qualifiers
plus convenience flags (`--owner`, `--language`, `--limit`, `--json`).

```bash
gh search repos "interactive fiction" --language python --stars ">100" --limit 20
gh search issues "stale save" --owner LO --state open
gh search prs --author "@me" --merged --limit 50
gh search code "checkSingleCondition" --owner LO --json path,repository
```

## Labels (`gh label`)

`list`, `create`, `edit`, `delete`, `clone` (copy a repo's labels to another).

```bash
gh label create blocked --color B60205 --description "Blocked on external work"
gh label clone OWNER/SOURCE_REPO          # copy labels into the current repo
gh label list
```

## Extensions (`gh extension`, alias `gh ext`)

`install`, `list`, `remove`, `upgrade`, `search`, `browse`, `create`, `exec`.
Extensions are GitHub repos named `gh-*` that add new top-level `gh` commands.

```bash
gh extension search dashboard
gh extension install dlvhdr/gh-dash        # then run: gh dash
gh extension list
gh extension upgrade --all
```

## Aliases (`gh alias`)

`set`, `list`, `delete`, `import`. Make shortcuts for long commands; `--shell`
runs an arbitrary shell command, and `$1`, `$@` accept arguments.

```bash
gh alias set prc 'pr create --fill'
gh alias set bugs 'issue list --label bug --state open'
gh alias set --shell wip '!git add -A && git commit -m wip && gh pr create --fill --draft'
gh alias list
```

## Config (`gh config`)

`get`, `set`, `list`, `clear-cache`. Tune editor, pager, default protocol, prompt.

```bash
gh config set editor "code --wait"
gh config set git_protocol ssh
gh config set pager "less -FX"
gh config list
```

## Other commands worth knowing

- **`gh browse`** — open the repo, a file, an issue/PR, or settings in the browser:
  `gh browse`, `gh browse 88`, `gh browse path/to/file.py:42`, `gh browse --settings`.
- **`gh status`** — a dashboard of issues, PRs, and notifications relevant to you
  across repos (`-e` to exclude repos, `-o` to scope to an org).
- **`gh org list`** — organizations you belong to.
- **`gh ruleset`** — `list`, `view`, `check` (which rules apply to a branch).
- **`gh ssh-key`** / **`gh gpg-key`** — `add`, `list`, `delete` keys on your account.
- **`gh attestation`** — verify/download artifact attestations (supply-chain).
- **`gh completion -s bash|zsh|fish|powershell`** — generate shell completions.
- **`gh copilot`** — GitHub Copilot CLI (preview), if installed/entitled.

## Targeting and host tips

- `-R OWNER/REPO` on any command, or `GH_REPO=OWNER/REPO`, or `gh repo set-default`
  — three ways to act on a repo you're not standing in.
- `--hostname ghe.example.com` or `GH_HOST` — point at GitHub Enterprise Server.
- For anything not covered here, `gh api` reaches the rest of the REST/GraphQL
  surface — see scripting.md.
