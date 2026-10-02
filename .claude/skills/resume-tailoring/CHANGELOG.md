# Changelog — resume-tailoring

## 2026-08-30 — installed from upstream

- Vendored from https://github.com/varunr89/resume-tailoring-skill @ v1.0.0
  (`.claude-plugin/plugin.json`), MIT, author Varun R.
- **Layout flattened on install.** Upstream ships `SKILL.md` under
  `skills/resume-tailoring/` while its four referenced companions
  (`research-prompts.md`, `matching-strategies.md`, `branching-questions.md`,
  `multi-job-workflow.md`) sit at the repo root. `SKILL.md:47-49,92` names them
  as siblings, so a straight `git clone` into a skills directory — which is what
  the upstream README still tells you to do — leaves every one of those four
  references dangling. Copied all five into this one directory instead.
- Also copied: `README.md`, `LICENSE`, `docs/` (plans, schemas, test checklist).
- Not copied: `MARKETPLACE.md`, `SUBMISSION_GUIDE.md`, `.gitignore` —
  marketplace-submission scaffolding, no bearing on running the skill.
- Companion workspace created at `resume/` (repo root), holding `resumes/` and
  `resumes/batches/` because the skill resolves its library as `resumes/`
  relative to cwd (`SKILL.md:33,164,232`; `multi-job-workflow.md:70`).
- Verified: frontmatter `name`/`description` present; all four sibling
  references resolve on disk.
