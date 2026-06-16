---
mode: agent
description: Phase 7 — Ship. Mechanical finalization; human approves merge.
---

# Punch — Ship

**Lifecycle phase:** Ship
**Mode:** Agent (mechanical operations only — no logic edits)
**Owner skill:** [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md)
(for the `git` + `gh` mechanics) +
[`punch-governance-review`](../skills/punch-governance-review/SKILL.md)
(for the readiness summary)
**Agent:** [`punch-reviewer`](../agents/punch-reviewer.agent.md)

## When to use

Review has approved the change. Ship handles the mechanical steps of
committing, pushing, opening a PR, **and producing a ship-readiness
summary**. Ship never merges, never tags releases, and never pushes
directly to `main`.

## Inputs

- The approved Review report.
- The branch and the target base branch (default `main`).
- The Verify evidence path.

## What to do

1. `git status` — confirm only expected files are modified.
2. `git add` the in-scope files explicitly (no `git add -A`, no
   `git add .`).
3. Compose a commit message:
   - One-line subject in imperative mood.
   - Body referencing the Plan task(s) in 2–3 lines.
   - No marketing language.
4. `git commit` — signing/hooks intact (never `--no-verify`).
5. `git push -u origin <branch>` if the branch is local.
6. `gh pr create` using `.github/PULL_REQUEST_TEMPLATE.md`'s checklist
   literally. The test plan section points at the Verify evidence.
7. Produce a **ship-readiness summary** (see below) and include it
   in the PR description or as a chat reply.
8. Return the PR URL.

## Ship-readiness summary

```
Summary: <one paragraph — what the change does and why>

Completed tasks:
  - <task ID — one-line goal>
  - ...

Validation status:
  - reports/state/punch-run.json: passed: <bool>
  - Tests run: <list>

Known risks:
  - <one-liner or "none">

Operational impact:
  - artifacts changed: <none, or contract entries>
  - service contract changed: <none, or details>
  - host requirements changed: <none, or details>

Documentation status: <updated / not applicable>

Recommendation: ship | hold
  Reason: <one sentence>
```

## What NOT to do

- Do not merge the PR. The human is the final approval gate.
- Do not push tags or trigger releases.
- Do not force-push or amend commits without explicit human approval.
- Do not skip hooks or signing.
- Do not introduce new code in Ship. Any "while I'm here" fix returns to
  Plan.

## Validation gate

The pipeline (GitHub Actions) re-runs Verify in CI. Human reviews the PR
and merges. Ship is complete when the PR is merged by a human.
