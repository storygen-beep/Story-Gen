# GitHub Actions from the terminal: `gh run`, `gh workflow`, `gh cache`, secrets & variables

Driving and debugging CI without leaving the shell. Command lists from
`gh <cmd> --help` (gh 2.86.0). All accept `-R/--repo`.

## Workflow runs (`gh run`)

| Subcommand | Purpose |
|---|---|
| `list` | Recent runs (filter `--workflow`, `--branch`, `--status`, `--user`, `--event`) |
| `view` | Inspect a run; `--log` full logs, `--log-failed` only failed steps, `--job ID` one job |
| `watch` | Block and stream a run until it finishes (exit non-zero if it fails) |
| `rerun` | Re-run (`--failed` only failed jobs, `--debug` with debug logging) |
| `cancel` | Cancel an in-progress run |
| `download` | Download artifacts (`-n NAME`, `-D DIR`) |
| `delete` | Delete a run |

The debugging loop — "why did CI fail?":

```bash
gh run list --workflow ci.yml --limit 5          # find the run, note its ID
gh run view 123456789                              # summary: which jobs/steps failed
gh run view 123456789 --log-failed                 # just the failing step output
gh run view 123456789 --job 987654321 --log        # full log for one job
gh run rerun 123456789 --failed                    # retry only what failed
```

Gate a script on a run, or watch the newest one:

```bash
gh run watch "$(gh run list --workflow ci.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run download 123456789 -n build-output -D ./artifacts
```

## Workflows (`gh workflow`)

| Subcommand | Purpose |
|---|---|
| `list` | List workflows (`--all` includes disabled) |
| `view` | Show a workflow + recent runs (`--yaml` prints the file) |
| `run` | Trigger a `workflow_dispatch` workflow |
| `enable` / `disable` | Turn a workflow on/off |

Manually trigger a dispatchable workflow, passing inputs:

```bash
gh workflow run deploy.yml --ref main -f environment=staging -f version=1.2.3
gh workflow run deploy.yml --ref main --json < inputs.json   # inputs from a JSON file on stdin
gh workflow view deploy.yml --yaml
```

`-f key=value` sets a string input; raw-typed inputs go through `--json` on stdin.
After triggering, find the run with `gh run list --workflow deploy.yml` and
`gh run watch`.

## Caches (`gh cache`)

| Subcommand | Purpose |
|---|---|
| `list` | List Actions caches (`--key`, `--ref`, `--order`, `--sort`) |
| `delete` | Delete a cache by id/key, or `--all` |

```bash
gh cache list --ref refs/heads/main
gh cache delete --all            # nuke all caches (e.g. to force a clean build)
```

## Secrets (`gh secret`) and variables (`gh variable`)

Secrets are encrypted and write-only; variables are plain and readable. Both live
at repo, environment, or org scope.

| `gh secret` | `gh variable` | Purpose |
|---|---|---|
| `set` | `set` | Create/update |
| `list` | `list` | List (secret values never shown) |
| `delete` | `delete` | Remove |
| — | `get` | Read a variable's value |

Scope flags: `--env ENV` (environment), `--org ORG` (org; add `--visibility`),
`--app actions|codespaces|dependabot` (which app the secret is for).

```bash
gh secret set DEPLOY_KEY < key.pem               # value from a file
gh secret set NPM_TOKEN --body "$NPM_TOKEN"      # value inline
gh secret set DB_URL --env production            # environment-scoped
gh secret list

gh variable set NODE_VERSION --body "20"
gh variable get NODE_VERSION
gh variable list --env staging
```

Never echo a secret value into your shell history or logs where you can avoid it
— prefer `< file` or `--body "$ENV_VAR"`.
