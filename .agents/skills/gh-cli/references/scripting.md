# Scripting with `gh`: JSON output, `gh api`, and pipelines

This is the part of `gh` that matters most for automation and agents. The goal is
to turn GitHub into structured data you can filter, reshape, and pipe — instead of
scraping human-formatted tables.

## Contents
- [The `--json` / `--jq` / `--template` triad](#the---json----jq----template-triad)
- [`gh api`: any REST endpoint](#gh-api-any-rest-endpoint)
- [Pagination](#pagination)
- [GraphQL](#graphql)
- [Exit codes and error handling](#exit-codes-and-error-handling)
- [Recipes](#recipes)

## The `--json` / `--jq` / `--template` triad

Many `list`/`view` commands accept `--json`. The rules (`gh help formatting` is
the source of truth):

1. `--json` **requires a comma-separated list of fields**. To discover the field
   names, run the command with `--json` and **no argument** — `gh` errors and
   prints every available field:
   ```bash
   gh pr list --json
   gh issue view 42 --json
   gh run list --json
   ```
2. Once you have JSON, shape it with **`--jq`** (jq syntax) or **`--template`**
   (Go templates). You must pass `--json` first; `--jq`/`--template` alone do
   nothing.

```bash
# Raw JSON (pipe to jq, save to a file, feed another tool)
gh pr list --json number,title,author,isDraft

# Filter inline with --jq (no external jq needed; it's built in)
gh pr list --json number,title,headRefName \
  --jq '.[] | select(.headRefName | startswith("feat/")) | .number'

# Reshape with a Go template for human-readable lines
gh run list --json databaseId,displayTitle,conclusion \
  --template '{{range .}}{{.databaseId}}  {{.conclusion}}  {{.displayTitle}}{{"\n"}}{{end}}'
```

`--jq` is usually the faster path. Use `--template` when you want `gh`'s template
helpers (`tablerow`, `timeago`, `color`) — see `gh help formatting`.

## `gh api`: any REST endpoint

When no porcelain command exists, call the API directly. `gh api` handles auth,
the base URL, and the `Accept` header for you.

```bash
gh api /user                                   # GET, authenticated
gh api repos/{owner}/{repo}/issues             # {owner}/{repo} auto-filled from cwd repo
gh api /repos/cli/cli/releases/latest --jq '.tag_name'
```

Key flags (verified, gh 2.86.0):
- `-X, --method` — HTTP method (default `GET`; sending fields implies `POST`).
- `-f, --raw-field key=value` — add a **string** field.
- `-F, --field key=value` — add a **typed** field (numbers/booleans/null parsed;
  `@file`/`@-` reads a value from a file or stdin). Use `-F` when the API expects
  a real integer/boolean, `-f` to force a string.
- `-H, --header key:value` — extra request header.
- `-q, --jq` / `-t, --template` — shape the response (same as above).
- `--paginate` — follow `Link` headers and fetch every page.
- `--slurp` — with `--paginate`, collect all pages into one JSON array/object.
- `-i, --include` — include status line + response headers.
- `--input file` (or `-`) — send a raw request body from a file/stdin.
- `--cache 1h` — cache the response locally for the given duration.

```bash
# Create an issue via the API with typed + string fields
gh api repos/{owner}/{repo}/issues \
  -f title="Found a bug" \
  -f body="Steps to reproduce..." \
  -F labels[]=bug -F labels[]=triage

# Send a JSON body from stdin
echo '{"title":"x","body":"y"}' | gh api repos/{owner}/{repo}/issues --input -
```

`{owner}`, `{repo}`, and `{branch}` placeholders are filled from the current
repo. Use `--hostname` (or `GH_HOST`) for Enterprise.

## Pagination

REST list endpoints return one page (default 30 items). Two ways to get them all:

```bash
gh api --paginate repos/{owner}/{repo}/issues --jq '.[].number'
gh api --paginate --slurp repos/{owner}/{repo}/issues   # one merged JSON array
```

Porcelain `list` commands page differently — they cap at 30 unless told otherwise:

```bash
gh pr list --limit 200
gh issue list --limit 500 --state all
```

`--slurp` matters because without it `--paginate` concatenates pages as separate
JSON documents, which most JSON consumers can't read.

## GraphQL

For data the REST API exposes awkwardly (or not at all), use GraphQL:

```bash
gh api graphql -f query='
  query($owner:String!, $name:String!) {
    repository(owner:$owner, name:$name) {
      pullRequests(states:OPEN, first:20) {
        nodes { number title author { login } }
      }
    }
  }' -F owner=cli -F name=cli --jq '.data.repository.pullRequests.nodes[].number'
```

GraphQL pagination uses cursors; `--paginate` understands them if your query
exposes a `pageInfo { hasNextPage endCursor }` and uses an `$endCursor` variable.

## Exit codes and error handling

`gh` returns a **non-zero exit code on failure**, so it's safe to use in
conditionals. Notable codes:
- `0` success, `1` general error, `2` cancel/usage, `4` auth required.
- Commands like `gh pr checks` exit non-zero if any check **failed/pending**, which
  is exactly what you want for gating in CI:
  ```bash
  if gh pr checks 123 --watch; then echo "all green"; else echo "CI not passing"; fi
  ```

When parsing, prefer `--jq`/`--json` over `grep` on human output — the table
format is for people and can change between versions; JSON fields are stable.

## Recipes

```bash
# Numbers of all open PRs targeting main, authored by me
gh pr list --base main --author "@me" --state open --json number --jq '.[].number'

# Watch the latest run of a workflow and fail the shell if it fails
gh run watch "$(gh run list --workflow ci.yml --limit 1 --json databaseId --jq '.[0].databaseId')"

# Bulk-close stale issues labeled wontfix
for n in $(gh issue list --label wontfix --state open --json number --jq '.[].number'); do
  gh issue close "$n" --reason "not planned"
done

# Get the default branch of any repo without cloning it
gh repo view OWNER/REPO --json defaultBranchRef --jq '.defaultBranchRef.name'

# Download the most recent successful build artifact
gh run download "$(gh run list --status success --limit 1 --json databaseId --jq '.[0].databaseId')"
```
