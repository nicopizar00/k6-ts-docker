---
mode: agent
description: Phase 6 — Ship. Mechanical finalization; human approves merge.
---

# Punch — Ship

**Lifecycle phase:** Ship
**Mode:** Agent (mechanical operations only)
**Owner skill:** `punch-orchestration`

## When to use

Review has approved the change. Ship handles the mechanical steps of
committing, pushing, and opening a PR. **Ship never merges, never tags
releases, and never pushes directly to `main`.**

## Inputs

- The approved Review note.
- The branch and the target base branch (default `main`).

## What to do

1. `git status` — confirm only expected files are modified.
2. `git add` the in-scope files explicitly (no `git add -A`).
3. Compose a commit message:
   - One-line subject in imperative mood.
   - Body referencing the Shape plan in 2–3 lines.
   - No marketing language.
4. `git commit` (signing/hooks left intact — never `--no-verify`).
5. `git push -u origin <branch>` if the branch is local.
6. `gh pr create` with the PR template's summary + test plan. Use the Verify
   evidence path as the test plan.
7. Return the PR URL.

## What NOT to do

- Do not merge the PR. The human is the final approval gate.
- Do not push tags or trigger releases.
- Do not force-push or amend commits without explicit human approval.
- Do not skip hooks or signing.

## Validation gate

The pipeline (GitHub Actions) re-runs Verify in CI. Human reviews the PR and
merges. Ship is complete when the PR is merged by a human.
